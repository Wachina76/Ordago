import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Pro - Vanesa", layout="wide")

# --- MOTOR LÓGICO ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'baraja': [],
        'descartadas': [], # Nueva lista para guardar lo que tiramos
        'lance_actual': None,
        'historial': "¡Mesa lista!"
    })

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 45px !important; border-radius: 4px; }
    .label-jugador { color: #FFD700; font-size: 0.7rem; text-align: center; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 5px; margin-bottom:5px;}
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px; border: 1px solid #0f0; min-height: 45px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN SEGURA DE BARAJA ---
def sacar_carta():
    if not st.session_state.baraja:
        # Si no hay cartas, mezclamos las descartadas
        st.session_state.baraja = st.session_state.descartadas.copy()
        random.shuffle(st.session_state.baraja)
        st.session_state.descartadas = []
        st.toast("Barajando descartes...")
    return st.session_state.baraja.pop(0)

def repartir():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    nums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
    random.shuffle(baraja)
    st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
    st.session_state.baraja = baraja[16:]
    st.session_state.descartadas = []
    st.session_state.estado = "MUS"
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

def ejecutar_descarte_ia_y_usuario(indices_usuario):
    # Guardamos las cartas que tira el usuario
    for i in indices_usuario:
        st.session_state.descartadas.append(st.session_state.partida['jugador'][i])
    
    # Reponemos mano del usuario
    mano_u = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in indices_usuario]
    while len(mano_u) < 4: mano_u.append(sacar_carta())
    st.session_state.partida['jugador'] = mano_u
    
    # Descarte IA
    for k in ['izq', 'arriba', 'der']:
        mano = st.session_state.partida[k]
        a_quitar = [c for c in mano if c['num'] not in [12, 1, 3, 2]]
        st.session_state.descartadas.extend(a_quitar) # Al pozo
        conservar = [c for c in mano if c['num'] in [12, 1, 3, 2]]
        while len(conservar) < 4: conservar.append(sacar_carta())
        st.session_state.partida[k] = conservar
    
    st.session_state.estado = "MUS"
    st.session_state.historial = "Descarte completado. ¿Sigue habiendo Mus?"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return []
    cols = st.columns(4)
    sel = []
    for i, c in enumerate(mano):
        with cols[i]:
            img_name = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", img_name)
            if os.path.exists(path): st.image(path)
            else: st.button("🎴", key=f"b_{clave}_{i}")
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.checkbox("Tirar", key=f"ch_{i}"): sel.append(i)
    return sel

# Mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mano('arriba', "PAREJA")
ci, cm, cd = st.columns([1, 1, 1])
with ci: dibujar_mano('izq', "RIVAL IZQ")
with cd: dibujar_mano('der', "RIVAL DER")
_, cy, _ = st.columns([1, 1, 1])
with cy: indices_desc = dibujar_mano('jugador', "VANESA (TÚ)", visible=True)

st.write("---")

if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("✅ PEDIR MUS", use_container_width=True):
        corta = any(any(c['num'] == 12 for c in st.session_state.partida[k]) for k in ['izq', 'der'])
        if corta and random.random() > 0.7:
            st.session_state.estado = "JUEGO"
            st.session_state.historial = "¡Rival CORTA! A lances."
        else:
            st.session_state.estado = "DESCARTE"
            st.session_state.historial = "Elige tus descartes."
        st.rerun()
    if c2.button("❌ CORTAR", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ DESCARTAR ({len(indices_desc)})", use_container_width=True):
        ejecutar_descarte_ia_y_usuario(indices_desc)
        st.rerun()

elif st.session_state.estado == "JUEGO":
    st.columns(4)[0].button("GRANDE", type="primary")
    if st.button("🔄 Nueva Mano", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.rerun()
