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

# --- CSS ULTRA COMPACTO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); overflow: hidden; }
    
    /* Contenedor de cartas solapadas */
    .mano-horizontal {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    .mano-horizontal img {
        width: 60px !important;
        margin-left: -20px; /* Solapamiento horizontal */
        border: 1px solid #444;
        box-shadow: 3px 0 5px rgba(0,0,0,0.3);
    }
    .mano-horizontal img:first-child { margin-left: 0; }

    .mano-vertical {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .mano-vertical img {
        width: 55px !important;
        margin-top: -35px; /* Solapamiento vertical */
        border: 1px solid #444;
    }
    .mano-vertical img:first-child { margin-top: 0; }

    .label-jugador {
        color: #FFD700;
        font-size: 0.75rem;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: rgba(0,0,0,0.3);
        padding: 2px 10px;
        border-radius: 10px;
        margin: 5px auto;
        width: fit-content;
    }
    
    /* Ajuste de márgenes de Streamlit */
    .block-container { padding-top: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE RENDERIZADO ---
def render_mano(mano, visible=False, modo="H"):
    if not mano: return
    
    html = f'<div class="{"mano-horizontal" if modo=="H" else "mano-vertical"}">'
    for carta in mano:
        if visible:
            num = str(carta['num']).zfill(2)
            fname = f"{num}-{carta['palo']}.png"
        else:
            fname = "reverso.png"
        
        path = os.path.join("img", fname)
        # Si no existe la imagen, usamos un marcador visual
        if os.path.exists(path):
            # Usamos base64 o ruta directa. En Streamlit local/cloud la ruta relativa suele bastar
            html += f'<img src="app/static/{path}" onerror="this.src=\'https://via.placeholder.com/60x90/8B0000/FFFFFF?text=X\'">'
        else:
            html += f'<img src="https://via.placeholder.com/60x90/222/FFF?text=🎴">'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- MESA ---
st.markdown("<h3 style='text-align:center; color:white; margin:0;'>🏆 ÓRDAGO</h3>", unsafe_allow_html=True)

if st.button("🧧 REPARTIR", use_container_width=True):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida = {
        'jugador': baraja[0:4], 'izq': baraja[4:8], 
        'arriba': baraja[8:12], 'der': baraja[12:16]
    }
    st.rerun()

# --- DISPOSICIÓN ---
# Arriba
st.markdown('<div class="label-jugador">Pareja</div>', unsafe_allow_html=True)
render_mano(st.session_state.partida['arriba'], visible=False, modo="H")

# Centro (Izquierda - Espacio - Derecha)
col_izq, col_mid, col_der = st.columns([1, 2, 1])
with col_izq:
    st.markdown('<div class="label-jugador">Rival Izq</div>', unsafe_allow_html=True)
    render_mano(st.session_state.partida['izq'], visible=False, modo="V")

with col_mid:
    # Espacio central para el mazo/puntos en el futuro
    st.write("")

with col_der:
    st.markdown('<div class="label-jugador">Rival Der</div>', unsafe_allow_html=True)
    render_mano(st.session_state.partida['der'], visible=False, modo="V")

# Abajo
st.markdown('<div class="label-jugador">Tu Mano</div>', unsafe_allow_html=True)
render_mano(st.session_state.partida['jugador'], visible=True, modo="H")

# Botones de juego rápidos
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
c1.button("PASO", use_container_width=True)
c2.button("ENVIDO", use_container_width=True)
c3.button("ÓRDAGO", use_container_width=True)
c4.button("QUIERO", use_container_width=True)
