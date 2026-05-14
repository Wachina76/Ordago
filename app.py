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
    st.session_state.partida = {'jugador': [], 'izquierda': [], 'derecha': [], 'arriba': []}

# --- CSS PARA CARTAS PEQUEÑAS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    
    /* Controlamos el tamaño máximo de la imagen */
    img {
        max-width: 80px !important; 
        margin: 0 auto;
        display: block;
        border-radius: 4px;
    }
    
    .nombre-jugador {
        color: #FFD700;
        text-align: center;
        font-size: 0.8rem;
        background: rgba(0,0,0,0.4);
        padding: 2px;
        margin-bottom: 5px;
        border-radius: 5px;
    }

    /* Reducir espacio entre columnas de Streamlit */
    [data-testid="column"] {
        padding: 0px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN RENDER ---
def mostrar_mano(mano, titulo):
    st.markdown(f"<div class='nombre-jugador'>{titulo}</div>", unsafe_allow_html=True)
    if mano:
        # Usamos 4 columnas muy juntas
        cols = st.columns(4)
        for i, carta in enumerate(mano):
            with cols[i]:
                num_str = str(carta['num']).zfill(2)
                nombre_archivo = f"{num_str}-{carta['palo']}.png"
                ruta = os.path.join("img", nombre_archivo)
                if os.path.exists(ruta):
                    st.image(ruta)
                else:
                    st.write(f"⚠️")

# --- MESA ---
st.title("🏆 ÓRDAGO")

if st.button("🧧 REPARTIR NUEVA MANO", use_container_width=True):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida['jugador'] = baraja[0:4]
    st.session_state.partida['izquierda'] = baraja[4:8]
    st.session_state.partida['arriba'] = baraja[8:12]
    st.session_state.partida['derecha'] = baraja[12:16]
    st.rerun()

# Disposición compacta
# Fila Arriba
_, centro_arriba, _ = st.columns([1, 1, 1])
with centro_arriba:
    mostrar_mano(st.session_state.partida['arriba'], "PAREJA")

# Fila Central
izq, mazo, der = st.columns([1, 0.5, 1])
with izq:
    mostrar_mano(st.session_state.partida['izquierda'], "RIVAL IZQ")
with mazo:
    st.write("") # Aquí irían los amarracos o el mazo
with der:
    mostrar_mano(st.session_state.partida['derecha'], "RIVAL DER")

# Fila Abajo
_, centro_abajo, _ = st.columns([1, 1, 1])
with centro_abajo:
    mostrar_mano(st.session_state.partida['jugador'], "TU MANO")

# Acciones pequeñas
st.write("---")
c1, c2, c3, c4 = st.columns(4)
c1.button("PASO", key="p")
c2.button("ENVIDO", key="e")
c3.button("ÓRDAGO", key="o")
c4.button("QUIERO", key="q")
