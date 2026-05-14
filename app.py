import streamlit as st
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mus Web", layout="centered")

# --- MOTOR INTERNO (Para evitar errores de importación) ---
def crear_baraja_simple():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    caras = ['R', '3', 'C', 'S', '7', '6', '5', '4', '2', 'A']
    return [{'cara': c, 'palo': p} for c in caras for p in palos]

# --- ESTADO DEL JUEGO ---
if 'marcador' not in st.session_state:
    st.session_state.marcador = {"Nosotros": 0, "Ellos": 0}
if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- INTERFAZ BONITA CON CSS ---
st.markdown("""
    <style>
    .carta {
        background-color: white;
        border: 2px solid #333;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        font-size: 25px;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        margin: 5px;
    }
    .Oros { color: #D4AF37; }
    .Copas { color: #D32F2F; }
    .Espadas { color: #1976D2; }
    .Bastos { color: #388E3C; }
    </style>
    """, unsafe_allow_html=True)

st.title("🃏 El Gran Mus")

# Marcador
col_m1, col_m2 = st.columns(2)
col_m1.metric("Puntos Nosotros", st.session_state.marcador["Nosotros"])
col_m2.metric("Puntos Ellos", st.session_state.marcador["Ellos"])

# Botón principal
if st.button("🎴 REPARTIR MANO"):
    baraja = crear_baraja_simple()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# Dibujar cartas si existen
if st.session_state.mano:
    st.subheader("Tus Cartas")
    cols = st.columns(4)
    iconos = {'Oros': '🟡', 'Copas': '🏆', 'Espadas': '⚔️', 'Bastos': '🌿'}
    
    for i, carta in enumerate(st.session_state.mano):
        palo = carta['palo']
        cara = carta['cara']
        with cols[i]:
            st.markdown(f"""
                <div class="carta {palo}">
                    {cara}<br>{iconos[palo]}
                </div>
            """, unsafe_allow_html=True)

st.divider()

# Botones de acción
if st.session_state.mano:
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("PASO"):
        st.toast("Has pasado")
    if c2.button("ENVIDO"):
        st.toast("¡ENVIDO!", icon="💰")
    if c3.button("ÓRDAGO"):
        st.toast("¡ÓRDAGO!", icon="🔥")
    if c4.button("MUZ"):
        st.balloons()
