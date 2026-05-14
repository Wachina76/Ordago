import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Órdago Mus", layout="wide")

# --- MOTOR ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'partida' not in st.session_state:
    st.session_state.partida = {'jugador': [], 'izq': [], 'der': [], 'arriba': []}

# --- CSS MEJORADO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    
    /* Cartas pequeñas */
    img {
        max-width: 70px !important; 
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    
    /* Estilo para cartas verticales en los lados */
    .vertical-cards img {
        margin-bottom: -40px; /* Efecto de cartas solapadas */
        transition: margin 0.3s;
    }
    .vertical-cards img:hover { margin-bottom: 5px; }

    .nombre {
        color: #FFD700;
        text-align: center;
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA MOSTRAR CARTAS ---
def mostrar_mano(mano, visible=False, orientacion="horizontal"):
    if not mano: return
    
    if orientacion == "horizontal":
        cols = st.columns(4)
        for i, carta in enumerate(mano):
            with cols[i]:
                if visible:
                    num_str = str(carta['num']).zfill(2)
                    ruta = os.path.join("img", f"{num_str}-{carta['palo']}.png")
                else:
                    ruta = os.path.join("img", "reverso.png")
                
                if os.path.exists(ruta):
                    st.image(ruta)
                else:
                    st.button("🎴", key=f"btn_{ruta}_{i}")

    else: # Orientación Vertical para los lados
        st.markdown('<div class="vertical-cards">', unsafe_allow_html=True)
        for i, carta in enumerate(mano):
            if visible:
                num_str = str(carta['num']).zfill(2)
                ruta = os.path.join("img", f"{num_str}-{carta['palo']}.png")
            else:
                ruta = os.path.join("img", "reverso.png")
            
            if os.path.exists(ruta):
                st.image(ruta)
            else:
                st.write("🎴")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MESA DE JUEGO ---
st.title("🏆 ÓRDAGO")

if st.button("🧧 REPARTIR NUEVA MANO", use_container_width=True):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida['jugador'] = baraja[0:4]
    st.session_state.partida['izq'] = baraja[4:8]
    st.session_state.partida['arriba'] = baraja[8:12]
    st.session_state.partida['der'] = baraja[12:16]
    st.rerun()

# DISTRIBUCIÓN DE LA MESA
# 1. Arriba: Pareja (Oculto)
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    st.markdown('<div class="nombre">PAREJA</div>', unsafe_allow_html=True)
    mostrar_mano(st.session_state.partida['arriba'], visible=False)

# 2. Centro: Izquierda, Mazo, Derecha
col_izq, col_mazo, col_der = st.columns([1, 2, 1])
with col_izq:
    st.markdown('<div class="nombre">RIVAL IZQ</div>', unsafe_allow_html=True)
    mostrar_mano(st.session_state.partida['izq'], visible=False, orientacion="vertical")

with col_mazo:
    st.write("") # Espacio para el mazo central

with col_der:
    st.markdown('<div class="nombre">RIVAL DER</div>', unsafe_allow_html=True)
    mostrar_mano(st.session_state.partida['der'], visible=False, orientacion="vertical")

# 3. Abajo: Tú (Visible)
_, centro_abajo, _ = st.columns([1, 1, 1])
with centro_abajo:
    st.markdown('<div class="nombre">TU MANO (VANESA)</div>', unsafe_allow_html=True)
    mostrar_mano(st.session_state.partida['jugador'], visible=True)

st.divider()
# Botones de juego
if st.session_state.partida['jugador']:
    b1, b2, b3, b4 = st.columns(4)
    b1.button("PASO", use_container_width=True)
    b2.button("ENVIDO", use_container_width=True)
    b3.button("ÓRDAGO", use_container_width=True)
    b4.button("ENSEÑAR CARTAS", use_container_width=True)
