import streamlit as st
import random
import os

# --- CONFIGURACIÓN DE MESA ---
st.set_page_config(page_title="Órdago Mus", layout="centered")

# --- MOTOR DE JUEGO ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    # El mus usa: 1 (As), 2, 3, 4, 5, 6, 7, 10 (Sota), 11 (Caballo), 12 (Rey)
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- ESTILO VISUAL (Tapete) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    h1 { color: #FFD700; text-align: center; text-shadow: 2px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

st.title("🃏 ÓRDAGO")

# --- BOTÓN DE REPARTIR ---
if st.button("🎴 BARAJAR Y REPARTIR", use_container_width=True):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# --- LÓGICA DE CARGA DE IMÁGENES ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            nombre_archivo = f"{carta['palo']}_{carta['num']}.png"
            
            # PROBAMOS TODAS LAS RUTAS POSIBLES
            posibles_rutas = [
                os.path.join("img", nombre_archivo),        # Opción 1: /img/oros_1.png
                os.path.join("mus", "img", nombre_archivo), # Opción 2: /mus/img/oros_1.png
                nombre_archivo                              # Opción 3: Raíz
            ]
            
            encontrada = False
            for ruta in posibles_rutas:
                if os.path.exists(ruta):
                    st.image(ruta, use_container_width=True)
                    encontrada = True
                    break
            
            if not encontrada:
                st.error(f"No veo {nombre_archivo}")
                st.caption(f"{carta['num']} de {carta['palo']}")

st.divider()

# --- ACCIONES ---
if st.session_state.mano:
    c1, c2, c3 = st.columns(3)
    c1.button("PASO", use_container_width=True)
    c2.button("ENVIDO", use_container_width=True)
    c3.button("ÓRDAGO", use_container_width=True)
