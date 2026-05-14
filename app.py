import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Realista", layout="centered")

# --- MOTOR INTERNO (Ajustado al repo de mcmd) ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    # En el Mus usamos: 1, 2, 3, 4, 5, 6, 7, 10 (Sota), 11 (Caballo), 12 (Rey)
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- ESTILO DE LA MESA ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .carta-marco {
        background-color: white;
        border-radius: 10px;
        padding: 4px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE CARGA SEGURA ---
def get_card_url(carta):
    # Esta es la URL "RAW" corregida del repositorio que pasaste
    base = "https://raw.githubusercontent.com/mcmd/playingcards.io-spanish.playing.cards/master/img"
    return f"{base}/{carta['palo']}_{carta['num']}.png"

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: gold;'>🏆 PARTIDA DE MUS</h1>", unsafe_allow_html=True)

if st.button("🧧 REPARTIR CARTAS", use_container_width=True):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# --- DIBUJAR CARTAS ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            url = get_card_url(carta)
            # El truco: Usamos el componente st.image nativo pero con una URL limpia
            st.image(url, use_container_width=True)
            st.caption(f"{carta['num']} de {carta['palo']}")

st.divider()

if st.session_state.mano:
    c1, c2, c3 = st.columns(3)
    c1.button("PASO", use_container_width=True)
    c2.button("ENVIDO", use_container_width=True)
    c3.button("ÓRDAGO", use_container_width=True)
