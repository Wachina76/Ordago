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

# --- CSS PARA FORZAR TAMAÑO Y ESPACIO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    
    /* Reducimos el tamaño de todas las imágenes de la mesa */
    [data-testid="stImage"] img {
        width: 50px !important; /* Cartas más pequeñas */
        border-radius: 4px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.4);
    }

    /* Quitamos el espacio exagerado entre columnas de Streamlit */
    [data-testid="column"] {
        padding: 0px 2px !important;
        display: flex;
        justify-content: center;
    }

    .label-jugador {
        color: #FFD700;
        font-size: 0.7rem;
        text-align: center;
        background: rgba(0,0,0,0.5);
        padding: 2px 8px;
        border-radius: 8px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE RENDERIZADO SEGURO ---
def mostrar_cartas_streamlit(mano, visible=False):
    if not mano: return
    # Creamos 4 columnas muy juntas
    cols = st.columns(4)
    for i, carta in enumerate(mano):
        with cols[i]:
            if visible:
                num = str(carta['num']).zfill(2)
                nombre = f"{num}-{carta['palo']}.png"
            else:
                nombre = "reverso.png"
            
            ruta = os.path.join("img", nombre)
            if os.path.exists(ruta):
                st.image(ruta)
            else:
                # Si falla la imagen, al menos vemos qué carta es
                st.code(f"{carta['num']}")

# --- MESA ---
st.markdown("<h4 style='text-align:center; color:white;'>🏆 ÓRDAGO</h4>", unsafe_allow_html=True)

if st.button("🧧 REPARTIR", use_container_width=True):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida = {
        'jugador': baraja[0:4], 'izq': baraja[4:8], 
        'arriba': baraja[8:12], 'der': baraja[12:16]
    }
    st.rerun()

# --- DISPOSICIÓN DE LA MESA ---

# 1. ARRIBA (PAREJA)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown('<div class="label-jugador">Pareja</div>', unsafe_allow_html=True)
    mostrar_cartas_streamlit(st.session_state.partida['arriba'], visible=False)

# 2. CENTRO (IZQ | MAZO | DER)
c_izq, c_mid, c_der = st.columns([1, 1, 1])
with c_izq:
    st.markdown('<div class="label-jugador">Rival Izq</div>', unsafe_allow_html=True)
    mostrar_cartas_streamlit(st.session_state.partida['izq'], visible=False)
with c_mid:
    st.write("") # Espacio mazo
with c_der:
    st.markdown('<div class="label-jugador">Rival Der</div>', unsafe_allow_html=True)
    mostrar_cartas_streamlit(st.session_state.partida['der'], visible=False)

# 3. ABAJO (TÚ)
_, c_yo, _ = st.columns([1, 1, 1])
with c_yo:
    st.markdown('<div class="label-jugador">Tu Mano</div>', unsafe_allow_html=True)
    mostrar_cartas_streamlit(st.session_state.partida['jugador'], visible=True)

st.divider()
# Botones compactos
btns = st.columns(4)
btns[0].button("PASO", use_container_width=True)
btns[1].button("ENVIDO", use_container_width=True)
btns[2].button("ÓRDAGO", use_container_width=True)
btns[3].button("QUIERO", use_container_width=True)
