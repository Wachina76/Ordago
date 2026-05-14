import streamlit as st
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mus Realista", layout="centered")

# --- MOTOR INTERNO ---
def crear_baraja():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    caras = ['R', '3', 'C', 'S', '7', '6', '5', '4', '2', 'A']
    return [{'cara': c, 'palo': p} for c in caras for p in palos]

# --- ESTADO DEL JUEGO ---
if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- DISEÑO CSS REALISTA ---
st.markdown("""
    <style>
    /* Tapete de casino */
    .stApp {
        background: radial-gradient(circle, #2e7d32 0%, #1b5e20 100%);
    }

    /* Contenedor de la carta física */
    .carta-real {
        position: relative;
        width: 130px;
        height: 200px;
        background-color: white;
        border-radius: 8px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5), 
                    inset 0 0 10px rgba(0,0,0,0.1);
        padding: 5px;
        transition: transform 0.2s ease-out;
        border: 1px solid #ccc;
    }

    .carta-real:hover {
        transform: translateY(-15px) rotate(2deg);
        box-shadow: 10px 20px 25px rgba(0,0,0,0.6);
    }

    /* Brillo de barniz sobre la carta */
    .carta-real::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 50%);
        border-radius: 8px;
        pointer-events: none;
    }

    .img-carta {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 5px;
    }

    /* Marcador elegante */
    .marcador {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA OBTENER IMAGEN REAL ---
def get_url_real(carta):
    p_map = {'Oros': 'oros', 'Copas': 'copas', 'Espadas': 'espadas', 'Bastos': 'bastos'}
    c_map = {'R': 12, 'C': 11, 'S': 10, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'A': 1}
    palo = p_map[carta['palo']]
    num = c_map[carta['cara']]
    # Usamos un repositorio de imágenes de alta calidad (Fournier Style)
    return f"https://raw.githubusercontent.com/saulmaldonado/spanish-deck/master/cards/{palo}_{num}.png"

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #ffd700; text-shadow: 2px 2px #000;'>🎴 MUS FOURNIER EDITION</h1>", unsafe_allow_html=True)

# Botón de reparto
if st.button("BARAJAR Y REPARTIR", use_container_width=True):
    baraja = crear_baraja()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# Mostrar cartas con realismo físico
if st.session_state.mano:
    st.write("")
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            url = get_url_real(carta)
            st.markdown(f"""
                <div class="carta-real">
                    <img src="{url}" class="img-carta">
                </div>
            """, unsafe_allow_html=True)

st.write("")
st.divider()

# Panel de control
if st.session_state.mano:
    c1, c2, c3 = st.columns(3)
    c1.button("PASO", use_container_width=True)
    c2.button("ENVIDO", use_container_width=True)
    c3.button("ÓRDAGO", use_container_width=True)
