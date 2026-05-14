import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Profesional", layout="centered")

# --- MOTOR INTERNO ---
def crear_baraja():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    caras = ['R', 'C', 'S', '7', '6', '5', '4', '3', '2', 'A']
    return [{'cara': c, 'palo': p} for c in caras for p in palos]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #265c26 0%, #123312 100%); }
    
    .carta-container {
        perspective: 1000px;
        margin-bottom: 20px;
    }
    
    .carta-img {
        width: 100%;
        border-radius: 8px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        transition: transform 0.3s;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .carta-img:hover {
        transform: translateY(-20px) rotate(2deg);
        box-shadow: 10px 30px 40px rgba(0,0,0,0.7);
    }

    .marcador-oro {
        text-align: center;
        color: #FFD700;
        font-family: 'serif';
        text-shadow: 2px 2px 4px #000;
        border: 2px solid #FFD700;
        padding: 10px;
        border-radius: 10px;
        background: rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE IMÁGENES (Servidor estable) ---
def obtener_url_carta(carta):
    # Usamos un servidor de imágenes especializado para juegos
    p_map = {'Oros': 'o', 'Copas': 'c', 'Espadas': 'e', 'Bastos': 'b'}
    c_map = {'R': '12', 'C': '11', 'S': '10', '7': '7', '6': '6', '5': '5', '4': '4', '3': '3', '2': '2', 'A': '1'}
    
    palo = p_map[carta['palo']]
    num = c_map[carta['cara']]
    
    # URL de un repositorio de cartas españolas optimizado para web
    return f"https://as01.epimg.net/img/comunes/fotos/diccionario/baraja/{palo}{num}.png"

# --- INTERFAZ ---
st.markdown("<div class='marcador-oro'><h1>🏆 GRAN CAMPEONATO DE MUS</h1></div>", unsafe_allow_html=True)
st.write("")

if st.button("🎴 BARAJAR Y REPARTIR", use_container_width=True):
    baraja = crear_baraja()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# --- MOSTRAR CARTAS ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            url = obtener_url_carta(carta)
            st.markdown(f"""
                <div class="carta-container">
                    <img src="{url}" class="carta-img">
                </div>
            """, unsafe_allow_html=True)

st.write("")
st.divider()

# Botones de juego profesionales
if st.session_state.mano:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("PASO", use_container_width=True)
    with c2: st.button("ENVIDO", use_container_width=True)
    with c3: st.button("ÓRDAGO", use_container_width=True)
    with c4: st.button("QUIERO", use_container_width=True)
