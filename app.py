import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Profesional", layout="centered")

# --- MOTOR INTERNO ---
def crear_baraja():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    caras = ['R', '3', 'C', 'S', '7', '6', '5', '4', '2', 'A']
    return [{'cara': c, 'palo': p} for c in caras for p in palos]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- ESTILOS CSS (Mesa y Cartas) ---
st.markdown("""
    <style>
    .stApp { background-color: #1a4a1a; }
    
    .carta-box {
        background-color: white;
        width: 140px;
        height: 210px;
        border-radius: 10px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        border: 2px solid #fff;
        transition: transform 0.3s;
    }
    
    .carta-box:hover {
        transform: translateY(-20px) rotate(2deg);
    }

    .img-real {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .marcador-web {
        background: rgba(0,0,0,0.3);
        padding: 20px;
        border-radius: 15px;
        color: gold;
        text-align: center;
        border: 1px solid gold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE IMÁGENES (Vía Wikimedia / Formato Seguro) ---
def obtener_url_wikimedia(carta):
    # Diccionario de nombres exactos en Wikimedia para la Baraja Española
    p_map = {'Oros': 'Oros', 'Copas': 'Copas', 'Espadas': 'Espadas', 'Bastos': 'Bastos'}
    c_map = {'R': '12', 'C': '11', 'S': '10', '7': '7', '6': '6', '5': '5', '4': '4', '3': '3', '2': '2', 'A': '1'}
    
    palo = p_map[carta['palo']]
    num = c_map[carta['cara']]
    
    # URL directa a archivos de alta disponibilidad
    return f"https://raw.githubusercontent.com/fede-pavon/baraja-espanola/master/cartas/{palo}_{num}.png"

# --- INTERFAZ DE USUARIO ---
st.markdown("<div class='marcador-web'><h1>🎴 CAMPEONATO DE MUS</h1></div>", unsafe_allow_html=True)

if st.button("🧧 BARAJAR Y REPARTIR", use_container_width=True):
    baraja = crear_baraja()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# --- MOSTRAR CARTAS ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            url = obtener_url_wikimedia(carta)
            # Usamos un contenedor HTML para forzar el diseño realista
            st.markdown(f"""
                <div class="carta-box">
                    <img src="{url}" class="img-real" onerror="this.src='https://via.placeholder.com/140x210?text={carta['cara']}+{carta['palo']}'">
                </div>
            """, unsafe_allow_html=True)

st.write("")
st.divider()

# Botones de juego
if st.session_state.mano:
    c1, c2, c3, c4 = st.columns(4)
    c1.button("PASO", use_container_width=True)
    c2.button("ENVIDO", use_container_width=True)
    c3.button("ÓRDAGO", use_container_width=True)
    c4.button("QUIERO", use_container_width=True)
