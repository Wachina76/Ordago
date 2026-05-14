import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Elite", layout="centered")

# --- MOTOR INTERNO ---
def crear_baraja():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    caras = ['R', '3', 'C', 'S', '7', '6', '5', '4', '2', 'A']
    return [{'cara': c, 'palo': p} for c in caras for p in palos]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- DISEÑO CSS DE ALTA CALIDAD (Sin imágenes externas) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e3311; } /* Verde tapete oscuro */
    
    .carta-pro {
        background: white;
        width: 130px;
        height: 200px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 15px;
        border: 1px solid #ccc;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .carta-pro:hover {
        transform: translateY(-15px);
        box-shadow: 0 20px 35px rgba(0,0,0,0.8);
    }

    .esquina {
        font-size: 22px;
        font-weight: 900;
        line-height: 1;
        font-family: 'Arial Black', sans-serif;
    }

    .simbolo-central {
        font-size: 65px;
        text-align: center;
        filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
    }

    /* Estilos por Palo */
    .palo-Oros { color: #b8860b; border-bottom: 8px solid #ffd700; }
    .palo-Copas { color: #d32f2f; border-bottom: 8px solid #ff5252; }
    .palo-Espadas { color: #1976d2; border-bottom: 8px solid #448aff; }
    .palo-Bastos { color: #2e7d32; border-bottom: 8px solid #66bb6a; }

    .nombre-palo {
        text-align: center;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: white;'>🃏 JUEGO DE MUS</h1>", unsafe_allow_html=True)

if st.button("🎴 REPARTIR NUEVA MANO", use_container_width=True):
    baraja = crear_baraja()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# --- DIBUJAR CARTAS ---
if st.session_state.mano:
    cols = st.columns(4)
    # Diccionario de símbolos de alta calidad
    simbolos = {'Oros': '🪙', 'Copas': '🏆', 'Espadas': '⚔️', 'Bastos': '🪵'}
    
    for i, carta in enumerate(st.session_state.mano):
        palo = carta['palo']
        cara = carta['cara']
        with cols[i]:
            st.markdown(f"""
                <div class="carta-pro palo-{palo}">
                    <div class="esquina">{cara}</div>
                    <div class="simbolo-central">{simbolos[palo]}</div>
                    <div class="nombre-palo">{palo}</div>
                </div>
            """, unsafe_allow_html=True)

st.write("")
st.divider()

# Botones de juego
if st.session_state.mano:
    c1, c2, c3 = st.columns(3)
    c1.button("PASO", use_container_width=True)
    c2.button("ENVIDO", use_container_width=True)
    c3.button("ÓRDAGO", use_container_width=True)
