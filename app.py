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
        import streamlit as st
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mus Deluxe", layout="centered")

# --- MOTOR INTERNO ---
def crear_baraja_simple():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    caras = ['R', '3', 'C', 'S', '7', '6', '5', '4', '2', 'A']
    return [{'cara': c, 'palo': p} for c in caras for p in palos]

# --- ESTADO DEL JUEGO ---
if 'marcador' not in st.session_state:
    st.session_state.marcador = {"Nosotros": 0, "Ellos": 0}
if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- DISEÑO DE ALTA CALIDAD (CSS) ---
st.markdown("""
    <style>
    /* Fondo de la mesa */
    .stApp {
        background-color: #1a4a1a;
        background-image: radial-gradient(#2d6a2d 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Contenedor de la carta */
    .carta-container {
        perspective: 1000px;
        display: inline-block;
    }
    
    .carta-diseno {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        border-radius: 12px;
        padding: 15px;
        width: 120px;
        height: 180px;
        text-align: center;
        border: 1px solid #ddd;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.3s;
        position: relative;
    }
    
    .carta-diseno:hover {
        transform: translateY(-10px);
    }

    .numero-esquina {
        position: absolute;
        top: 8px;
        left: 8px;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Georgia', serif;
    }

    .palo-central {
        font-size: 50px;
        margin-top: 20px;
    }

    .palo-nombre {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: bold;
    }

    /* Colores por palo */
    .Oros { color: #b8860b; border-top: 5px solid #ffd700; }
    .Copas { color: #d32f2f; border-top: 5px solid #ff5252; }
    .Espadas { color: #1976d2; border-top: 5px solid #448aff; }
    .Bastos { color: #2e7d32; border-top: 5px solid #66bb6a; }
    
    /* Marcador elegante */
    .marcador-caja {
        background: rgba(0,0,0,0.5);
        padding: 15px;
        border-radius: 15px;
        color: white;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO Y MARCADOR ---
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>🃏 MUS DELUXE</h1>", unsafe_allow_html=True)

m1, m2 = st.columns(2)
with m1:
    st.markdown(f"<div class='marcador-caja'><h3>Nosotros</h3><h2>{st.session_state.marcador['Nosotros']}</h2></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='marcador-caja'><h3>Ellos</h3><h2>{st.session_state.marcador['Ellos']}</h2></div>", unsafe_allow_html=True)

st.write("") # Espaciador

# --- ACCIÓN REPARTIR ---
if st.button("🎴 BARAJAR Y REPARTIR", use_container_width=True):
    with st.spinner('Barajando...'):
        baraja = crear_baraja_simple()
        random.shuffle(baraja)
        st.session_state.mano = baraja[:4]
        time_sleep = 0.5 # Simulación de reparto
    st.rerun()

# --- MOSTRAR MANO ---
if st.session_state.mano:
    cols = st.columns(4)
    iconos = {'Oros': '🟡', 'Copas': '🏆', 'Espadas': '⚔️', 'Bastos': '🌿'}
    
    for i, carta in enumerate(st.session_state.mano):
        palo = carta['palo']
        cara = carta['cara']
        with cols[i]:
            st.markdown(f"""
                <div class="carta-container">
                    <div class="carta-diseno {palo}">
                        <div class="numero-esquina">{cara}</div>
                        <div class="palo-central">{iconos[palo]}</div>
                        <div class="palo-nombre">{palo}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.write("")
st.divider()

# --- BOTONES DE JUEGO MEJORADOS ---
if st.session_state.mano:
    st.markdown("<h4 style='color: white;'>Tus jugadas:</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("PASO", use_container_width=True):
        st.toast("Has pasado esta ronda.")
    if c2.button("ENVIDO", use_container_width=True):
        st.toast("¡Has envidado!", icon="💰")
    if c3.button("ÓRDAGO", use_container_width=True):
        st.toast("¡A TODO O NADA!", icon="🔥")
    if c4.button("QUIERO", use_container_width=True):
        st.success("¡Aceptas el envite!")
