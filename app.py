import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Pro - Apuestas", layout="wide")

# --- MOTOR LÓGICO ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'baraja': [],
        'lance_actual': None,
        'historial': "¡Mesa lista!"
    })

# --- CSS MEJORADO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 46px !important; border-radius: 4px; }
    .label-jugador { color: #FFD700; font-size: 0.7rem; text-align: center; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 5px; margin-bottom:5px;}
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px; border: 1px solid #0f0; min-height: 45px; margin-bottom: 10px;}
    .boton-apuesta { margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES (REPARTO Y DESCARTE IGUAL QUE ANTES) ---
def repartir():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    nums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
    random.shuffle(baraja)
    st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
    st.session_state.baraja = baraja[16:]
    st.session_state.estado = "MUS"
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

def dibujar_mesa(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            fname = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", fname)
            if os.path.exists(path): st.image(path)
            else: st.button("🎴", key=f"c_{clave}_{i}")

# Dibujado de la mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mesa('arriba', "PAREJA")
ci, cm, cd = st.columns([1, 1, 1])
with ci: dibujar_mesa('izq', "RIVAL IZQ")
with cd: dibujar_mesa('der', "RIVAL DER")
_, cy, _ = st.columns([1, 1, 1])
with cy: dibujar_mesa('jugador', "TU MANO", visible=True)

st.write("---")

# --- LÓGICA DE BOTONES ---
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("✅ MUS", use_container_width=True):
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if c2.button("❌ CORTO", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    # Fila 1: Selección de Lance
    st.markdown("<p style='color:white; font-size:0.8rem; margin:0;'>Selecciona Lance:</p>", unsafe_allow_html=True)
    cols_l = st.columns(4)
    lances = ["GRANDE", "CHICA", "PARES", "JUEGO"]
    for i, l in enumerate(lances):
        if cols_l[i].button(l, use_container_width=True, type="primary" if st.session_state.lance_actual == l else "secondary"):
            st.session_state.lance_actual = l
            st.session_state.historial = f"Lance: {l}. ¿Qué quieres hacer?"
            st.rerun()

    # Fila 2: Acciones de Apuesta (Solo si hay un lance seleccionado)
    if st.session_state.lance_actual:
        st.markdown(f"<p style='color:#FFD700; text-align:center;'>Apuestas para {st.session_state.lance_actual}</p>", unsafe_allow_html=True)
        row1 = st.columns(4)
        if row1[0].button("PASO", use_container_width=True):
            st.session_state.historial = f"Has pasado en {st.session_state.lance_actual}."
        if row1[1].button("ENVIDO", use_container_width=True):
            st.session_state.historial = "¡Envido! Esperando respuesta del rival..."
        if row1[2].button("ÓRDAGO", use_container_width=True):
            st.session_state.historial = "¡ÓRDAGO! La partida se decide aquí."
        if row1[3].button("QUIERO", use_container_width=True):
            st.session_state.historial = "¡Quiero! Se verán las cartas al final."

        # Fila 3: Cantidades
        st.write("Aumentar apuesta:")
        row2 = st.columns(3)
        if row2[0].button("+2 Tantos", use_container_width=True):
            st.session_state.historial = f"Subes 2 tantos en {st.session_state.lance_actual}."
        if row2[1].button("+5 Tantos", use_container_width=True):
            st.session_state.historial = f"Subes 5 tantos en {st.session_state.lance_actual}."
        if row2[2].button("+10 Tantos", use_container_width=True):
            st.session_state.historial = f"Subes 10 tantos en {st.session_state.lance_actual}."

    if st.button("🔄 Nueva Mano", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.session_state.lance_actual = None
        st.rerun()
