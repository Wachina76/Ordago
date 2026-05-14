import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Pro - Descarte", layout="wide")

# --- MOTOR LÓGICO ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'baraja': [],
        'historial': "¡Mesa lista!"
    })

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 45px !important; border-radius: 4px; }
    .label-jugador { color: #FFD700; font-size: 0.75rem; text-align: center; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 5px; margin-bottom:5px;}
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px; border: 1px solid #0f0; margin-bottom: 15px; }
    div[data-testid="stCheckbox"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE JUEGO ---
def repartir_inicial():
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida = {
        'jugador': baraja[0:4], 'izq': baraja[4:8], 
        'arriba': baraja[8:12], 'der': baraja[12:16]
    }
    st.session_state.baraja = baraja[16:]
    st.session_state.estado = "MUS"
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

def ejecutar_descarte(indices_a_quitar):
    # 1. Tu descarte
    mano_nueva = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in indices_a_quitar]
    while len(mano_nueva) < 4:
        mano_nueva.append(st.session_state.baraja.pop(0))
    st.session_state.partida['jugador'] = mano_nueva

    # 2. Descarte de la IA (Rápido)
    # Lógica simple: La IA tira todo lo que no sea Rey (12), Tres (3), As (1) o Dos (2)
    for clave in ['izq', 'der', 'arriba']:
        mano = st.session_state.partida[clave]
        mano_conservada = [c for c in mano if c['num'] in [12, 1, 3, 2]]
        while len(mano_conservada) < 4:
            mano_conservada.append(st.session_state.baraja.pop(0))
        st.session_state.partida[clave] = mano_conservada

    st.session_state.estado = "MUS"
    st.session_state.historial = "Descarte completado. ¿Vuelve a haber Mus?"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

# Mesa
def dibujar_jugador(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    cols = st.columns(4)
    descartes = []
    for i, c in enumerate(mano):
        with cols[i]:
            nombre = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            ruta = os.path.join("img", nombre)
            if os.path.exists(ruta): st.image(ruta)
            else: st.code(f"{c['num']}")
            # Solo ponemos checkboxes en tu mano y si estamos en fase de descarte
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.checkbox("Tirar", key=f"chk_{i}"):
                    descartes.append(i)
    return descartes

# Layout
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_jugador('arriba', "PAREJA")

c_izq, c_mid, c_der = st.columns([1, 1, 1])
with c_izq: dibujar_jugador('izq', "RIVAL IZQ")
with c_der: dibujar_jugador('der', "RIVAL DER")

_, c_yo, _ = st.columns([1, 1, 1])
with c_yo: 
    indices_descarte = dibujar_jugador('jugador', "TU MANO (VANESA)", visible=True)

# --- BOTONES DE CONTROL ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        repartir_inicial()
        st.rerun()

elif st.session_state.estado == "MUS":
    col_a, col_b = st.columns(2)
    if col_a.button("✅ PEDIR MUS", use_container_width=True):
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if col_b.button("❌ NO HAY MUS", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    st.warning("Selecciona las cartas que quieres cambiar y pulsa el botón:")
    if st.button(f"♻️ DESCARTAR {len(indices_descarte)} CARTAS", use_container_width=True):
        ejecutar_descarte(indices_descarte)
        st.rerun()

elif st.session_state.estado == "JUEGO":
    st.success("¡Comienzan los lances!")
    if st.button("🔄 Nueva Mano"):
        st.session_state.estado = "INICIO"
        st.rerun()
