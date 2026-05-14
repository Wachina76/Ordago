import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Órdago Mus", layout="centered")

# --- MOTOR INTERNO ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    # El mus usa 1, 2, 3, 4, 5, 6, 7, 10 (Sota), 11 (Caballo), 12 (Rey)
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🃏 Órdago: El Juego de Mus")

if st.button("🎴 REPARTIR CARTAS"):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# --- MOSTRAR CARTAS LOCALES ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            # RUTA CLAVE: Como app.py está en la carpeta 'mus', 
            # buscamos la carpeta 'img' que está a su lado.
            nombre_archivo = f"{carta['palo']}_{carta['num']}.png"
            ruta_imagen = os.path.join("mus", "img", nombre_archivo)
            
            if os.path.exists(ruta_imagen):
                st.image(ruta_imagen, use_container_width=True)
            else:
                st.error(f"Falta: {nombre_archivo}")
                st.write(f"Cara: {carta['num']} de {carta['palo']}")

st.divider()

if st.session_state.mano:
    c1, c2, c3 = st.columns(3)
    c1.button("PASO")
    c2.button("ENVIDO")
    c3.button("ÓRDAGO")
