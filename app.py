import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Real", layout="centered")

# --- MOTOR INTERNO ---
def crear_baraja():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    # En ese repo, las cartas van del 1 al 12 (10=Sota, 11=Caballo, 12=Rey)
    numeros = range(1, 13)
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #165216; }
    
    .carta-realista {
        width: 100%;
        border-radius: 8px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    
    .carta-realista:hover {
        transform: scale(1.05) translateY(-10px);
    }
    
    .boton-repartir {
        background-color: #ffd700 !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA EL ENLACE DE GITHUB ---
def obtener_url_raw(carta):
    # La estructura del repo que pasaste es: img/palo_numero.png
    base_url = "https://raw.githubusercontent.com/mcmd/playingcards.io-spanish.playing.cards/master/img"
    return f"{base_url}/{carta['palo']}_{carta['num']}.png"

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: white;'>🎴 PARTIDA REALISTA</h1>", unsafe_allow_html=True)

if st.button("BARAJAR Y REPARTIR", use_container_width=True):
    baraja = crear_baraja()
    # El Mus se juega con 40 cartas (quitamos 8 y 9)
    # Filtramos para que solo salgan 1-7 y 10-12
    baraja_mus = [c for c in baraja if c['num'] not in [8, 9]]
    random.shuffle(baraja_mus)
    st.session_state.mano = baraja_mus[:4]
    st.rerun()

# --- MOSTRAR CARTAS ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            url = obtener_url_raw(carta)
            # Usamos st.image con la URL raw
            st.image(url, use_container_width=True)
            # Un pequeño texto debajo para confirmar
            nombre_carta = f"{carta['num']} de {carta['palo'].capitalize()}"
            st.markdown(f"<p style='color:white; text-align:center; font-size:12px;'>{nombre_carta}</p>", unsafe_allow_html=True)

st.divider()

# Botones de juego
if st.session_state.mano:
    c1, c2, c3 = st.columns(3)
    c1.button("PASO", use_container_width=True)
    c2.button("ENVIDO", use_container_width=True)
    c3.button("ÓRDAGO", use_container_width=True)
