import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Órdago Mus Pro", layout="wide")

# --- MOTOR DE CARTAS ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

# --- INICIALIZACIÓN DE MEMORIA (Session State) ---
if 'estado' not in st.session_state:
    st.session_state.estado = "INICIO" # INICIO, MUS, JUEGO
if 'partida' not in st.session_state:
    st.session_state.partida = {'jugador': [], 'izq': [], 'der': [], 'arriba': []}
if 'historial' not in st.session_state:
    st.session_state.historial = "Esperando a repartir..."

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 45px !important; border-radius: 4px; }
    .label-jugador { color: #FFD700; font-size: 0.7rem; text-align: center; background: rgba(0,0,0,0.5); padding: 2px 8px; border-radius: 8px; margin-bottom: 5px; }
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px; border: 1px solid #333; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE ACCIÓN ---
def repartir_todo():
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida = {
        'jugador': baraja[0:4], 'izq': baraja[4:8], 
        'arriba': baraja[8:12], 'der': baraja[12:16]
    }
    st.session_state.estado = "MUS"
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

def decision_ia():
    # Lógica simple: Los rivales siempre quieren mus si no tienen jugada grande
    rivales = ["Rival Izq", "Rival Der", "Pareja"]
    for r in rivales:
        # Aquí podrías meter lógica real de Mus
        pass
    st.session_state.historial = "La IA está esperando tu decisión..."

# --- RENDERIZADO DE CARTAS ---
def mostrar_cartas(mano, visible=False):
    if not mano: return
    cols = st.columns(4)
    for i, carta in enumerate(mano):
        with cols[i]:
            nombre = f"{str(carta['num']).zfill(2)}-{carta['palo']}.png" if visible else "reverso.png"
            ruta = os.path.join("img", nombre)
            if os.path.exists(ruta): st.image(ruta)
            else: st.code(f"{carta['num']}")

# --- INTERFAZ ---
st.title("🏆 MESA DE MUS INTELIGENTE")

# Consola de avisos
st.markdown(f'<div class="consola">{st.session_state.historial}</div>', unsafe_allow_html=True)
st.write("")

# REPARTO (Solo si estamos en inicio o terminó la mano)
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR CARTAS", use_container_width=True):
        repartir_todo()
        st.rerun()

# --- DISPOSICIÓN ---
c1, c2, c3 = st.columns([1, 1, 1])
with c2: # ARRIBA
    st.markdown('<div class="label-jugador">Pareja</div>', unsafe_allow_html=True)
    mostrar_cartas(st.session_state.partida['arriba'], visible=False)

c_izq, c_mid, c_der = st.columns([1, 1, 1])
with c_izq: # IZQ
    st.markdown('<div class="label-jugador">Rival Izq</div>', unsafe_allow_html=True)
    mostrar_cartas(st.session_state.partida['izq'], visible=False)
with c_der: # DER
    st.markdown('<div class="label-jugador">Rival Der</div>', unsafe_allow_html=True)
    mostrar_cartas(st.session_state.partida['der'], visible=False)

_, c_yo, _ = st.columns([1, 1, 1])
with c_yo: # TÚ
    st.markdown('<div class="label-jugador">Vanesa (Tú)</div>', unsafe_allow_html=True)
    mostrar_cartas(st.session_state.partida['jugador'], visible=True)

# --- BOTONES DE DECISIÓN ---
st.divider()
if st.session_state.estado == "MUS":
    col_a, col_b = st.columns(2)
    if col_a.button("✅ PEDIR MUS", use_container_width=True):
        st.session_state.historial = "Has pedido Mus. Los rivales están pensando..."
        # Aquí llamaríamos a una función que simula el descarte
    if col_b.button("❌ NO HAY MUS (CORTAR)", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.session_state.historial = "¡CORTADO! Empiezan los lances: Grande, Chica..."
        st.rerun()

if st.session_state.estado == "JUEGO":
    cols_j = st.columns(4)
    cols_j[0].button("GRANDE")
    cols_j[1].button("CHICA")
    cols_j[2].button("PARES")
    cols_j[3].button("JUEGO")
    if st.button("🔄 Reiniciar Mesa"):
        st.session_state.estado = "INICIO"
        st.rerun()
