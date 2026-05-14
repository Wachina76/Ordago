import streamlit as st
import random
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Órdago Mus Elite", layout="wide")

# --- MOTOR DE JUEGO ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'partida' not in st.session_state:
    st.session_state.partida = {
        'jugador': [], 'izquierda': [], 'derecha': [], 'arriba': []
    }

# --- ESTILO DE LA MESA ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .nombre-jugador {
        color: #FFD700;
        text-align: center;
        background: rgba(0,0,0,0.5);
        border-radius: 10px;
        padding: 5px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .carta-mesa { border-radius: 5px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA RENDERIZAR MANOS ---
def mostrar_mano(mano, titulo):
    st.markdown(f"<div class='nombre-jugador'>{titulo}</div>", unsafe_allow_html=True)
    if mano:
        cols = st.columns(4)
        for i, carta in enumerate(mano):
            with cols[i]:
                num_str = str(carta['num']).zfill(2)
                nombre_archivo = f"{num_str}-{carta['palo']}.png"
                ruta = os.path.join("img", nombre_archivo)
                if os.path.exists(ruta):
                    st.image(ruta, use_container_width=True)
                else:
                    st.caption(f"{carta['num']}-{carta['palo']}")

# --- CABECERA ---
st.title("🏆 GRAN MESA DE MUS")

if st.button("🧧 REPARTIR A TODA LA MESA", use_container_width=True):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida['jugador'] = baraja[0:4]
    st.session_state.partida['izquierda'] = baraja[4:8]
    st.session_state.partida['arriba'] = baraja[8:12]
    st.session_state.partida['derecha'] = baraja[12:16]
    st.rerun()

# --- DISPOSICIÓN DE LA MESA ---
# Fila Superior: Rival Arriba
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    mostrar_mano(st.session_state.partida['arriba'], "PAREJA (ARRIBA)")

# Fila Central: Izquierda y Derecha
col_izq, col_centro, col_der = st.columns([2, 1, 2])
with col_izq:
    mostrar_mano(st.session_state.partida['izquierda'], "RIVAL IZQUIERDA")
with col_centro:
    st.write("") # Espacio para el mazo o tanteo en el futuro
with col_der:
    mostrar_mano(st.session_state.partida['derecha'], "RIVAL DERECHA")

# Fila Inferior: Tú
c_a, c_b, c_c = st.columns([1, 2, 1])
with c_b:
    mostrar_mano(st.session_state.partida['jugador'], "TU MANO (VANESA)")

st.divider()

# Botones de acción (solo si hay cartas)
if st.session_state.partida['jugador']:
    ac1, ac2, ac3, ac4 = st.columns(4)
    ac1.button("PASO")
    ac2.button("ENVIDO")
    ac3.button("ÓRDAGO")
    ac4.button("QUIERO")
