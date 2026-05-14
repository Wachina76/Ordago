import streamlit as st
import random
import os
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Instantáneo", layout="wide")

# --- MOTOR LÓGICO ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'historial': "¡Mesa lista! Reparte para empezar."
    })

# --- CSS COMPACTO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 42px !important; border-radius: 3px; }
    .label-jugador { color: #FFD700; font-size: 0.7rem; text-align: center; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 5px; }
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 8px; border-radius: 5px; border: 1px solid #0f0; font-size: 0.85rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ACCIONES RÁPIDAS ---
def realizar_reparto():
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida = {
        'jugador': baraja[0:4], 'izq': baraja[4:8], 
        'arriba': baraja[8:12], 'der': baraja[12:16]
    }
    st.session_state.estado = "MUS"
    st.session_state.historial = "Cartas en la mesa. ¿Qué haces?"

def procesar_mus_ia(accion_usuario):
    if accion_usuario == "CORTAR":
        st.session_state.estado = "LANCES"
        st.session_state.historial = "¡Cortaste el mus! Empezamos con la GRANDE."
    else:
        # La IA decide INSTANTÁNEAMENTE
        # Lógica: Si alguien tiene una pareja de Reyes o 31, corta el mus.
        corta = False
        quien_corta = ""
        
        for rival, clave in [("Rival Izq", "izq"), ("Pareja", "arriba"), ("Rival Der", "der")]:
            mano = st.session_state.partida[clave]
            # Simulación de decisión rápida
            if any(c['num'] in [12, 1] for c in mano) and random.random() > 0.7:
                corta = True
                quien_corta = rival
                break
        
        if corta:
            st.session_state.estado = "LANCES"
            st.session_state.historial = f"{quien_corta} ha cortado el Mus. ¡A jugar!"
        else:
            st.session_state.historial = "Todos han pedido Mus. ¡Descarte general!"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

# MESA COMPACTA
def dibujar_mano(clave, visible=False, titulo=""):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if mano:
        cols = st.columns(4)
        for i, c in enumerate(mano):
            nombre = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            ruta = os.path.join("img", nombre)
            with cols[i]:
                if os.path.exists(ruta): st.image(ruta)
                else: st.code(f"{c['num']}")

# Layout de mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mano('arriba', False, "PAREJA")

c_izq, c_mid, c_der = st.columns([1, 1, 1])
with c_izq: dibujar_mano('izq', False, "RIVAL IZQ")
with c_der: dibujar_mano('der', False, "RIVAL DER")

_, c_yo, _ = st.columns([1, 1, 1])
with c_yo: dibujar_mano('jugador', True, "TU MANO")

# --- BOTONES DE ACCIÓN VELOZ ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        realizar_reparto()
        st.rerun()

elif st.session_state.estado == "MUS":
    col_a, col_b = st.columns(2)
    if col_a.button("✅ MUS", use_container_width=True):
        procesar_mus_ia("MUS")
        st.rerun()
    if col_b.button("❌ CORTO", use_container_width=True):
        procesar_mus_ia("CORTAR")
        st.rerun()

elif st.session_state.estado == "LANCES":
    l1, l2, l3, l4 = st.columns(4)
    l1.button("GRANDE")
    l2.button("CHICA")
    l3.button("PARES")
    l4.button("JUEGO")
    if st.button("🔄 Nueva Mano", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.rerun()
