import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Oficial Fournier - Recuento", layout="wide")

# --- MOTOR DE REGLAS ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'baraja': [],
        'descartadas': [],
        'lance_idx': 0,
        'historial': "Bienvenido al Mus. Las cartas se verán al final.",
        'es_mano': 'izq'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 50px !important; border-radius: 4px; border: 1px solid #555; }
    .label-jugador { color: #FFD700; font-size: 0.8rem; text-align: center; background: rgba(0,0,0,0.6); padding: 4px; border-radius: 5px; margin-bottom: 5px;}
    .consola-central { 
        background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; 
        padding: 20px; border-radius: 10px; border: 2px solid #FFD700; 
        text-align: center; min-height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-weight: bold; font-size: 1.2rem;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES LÓGICAS ---
def valor_fournier(n):
    if n == 3: return 12 # 3 es Rey
    if n == 2: return 1  # 2 es As
    return n

def sacar_carta():
    if not st.session_state.baraja:
        st.session_state.baraja = st.session_state.descartadas.copy()
        random.shuffle(st.session_state.baraja)
        st.session_state.descartadas = []
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
    st.session_state.lance_idx = 0
    st.session_state.historial = "Mano servida. ¿Hay Mus?"

def avanzar_lance():
    st.session_state.lance_idx += 1
    if st.session_state.lance_idx >= len(LANCES):
        st.session_state.estado = "REVELAR"
        st.session_state.historial = "¡A ver las caras! Recuento de tantos."
    else:
        st.session_state.historial += f" | Siguiente: {LANCES[st.session_state.lance_idx]}"

# --- INTERFAZ ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False):
    mano_mark = " ✋" if st.session_state.es_mano == clave else ""
    st.markdown(f'<div class="label-jugador">{titulo}{mano_mark}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return []
    cols = st.columns(4)
    sel = []
    for i, c in enumerate(mano):
        with cols[i]:
            fname = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", fname)
            if os.path.exists(path): st.image(path)
            else: st.button("🎴", key=f"v_{clave}_{i}")
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.checkbox("Tirar", key=f"s_{i}"): sel.append(i)
    return sel

# Mesa Visual
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mano('arriba', "PAREJA", visible=(st.session_state.estado == "REVELAR"))
ci, cm, cd = st.columns([1, 1.5, 1])
with ci: dibujar_mano('izq', "RIVAL IZQ", visible=(st.session_state.estado == "REVELAR"))
with cm: st.markdown(f'<div class="consola-central"><b>{st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with cd: dibujar_mano('der', "RIVAL DER", visible=(st.session_state.estado == "REVELAR"))
_, cy, _ = st.columns([1, 1, 1])
with cy: indices_descarte = dibujar_mano('jugador', "VANESA (TÚ)", visible=True)

st.write("---")

# --- ACCIONES ---
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ MUS", use_container_width=True):
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if col2.button("❌ CORTO", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CONFIRMAR DESCARTE ({len(indices_descarte)})", use_container_width=True):
        nuevas = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in indices_descarte]
        for i in indices_descarte: st.session_state.descartadas.append(st.session_state.partida['jugador'][i])
        while len(nuevas) < 4: nuevas.append(sacar_carta())
        st.session_state.partida['jugador'] = nuevas
        # Descartes IA
        for k in ['izq', 'arriba', 'der']:
            m = st.session_state.partida[k]
            cons = [c for c in m if c['num'] in [12, 1, 3, 2]]
            while len(cons) < 4: cons.append(sacar_carta())
            st.session_state.partida[k] = cons
        st.session_state.estado = "MUS"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    b1, b2, b3 = st.columns(3)
    if b1.button("PASO", use_container_width=True):
        st.session_state.historial = f"Paso en {LANCES[st.session_state.lance_idx]}."
        avanzar_lance()
        st.rerun()
    if b2.button("ENVIDO", use_container_width=True):
        if random.random() > 0.4:
            st.session_state.historial = "¡Rival QUIERE!"
        else:
            st.session_state.historial = "Rival NO QUIERE. +1 punto."
            st.session_state.puntos['nosotros'] += 1
        avanzar_lance()
        st.rerun()
    if b3.button("ÓRDAGO", use_container_width=True):
        st.session_state.historial = "¡Rival NO QUIERE el Órdago! +1 punto."
        st.session_state.puntos['nosotros'] += 1
        avanzar_lance()
        st.rerun()

elif st.session_state.estado == "REVELAR":
    st.success("Recuento finalizado basado en las cartas mostradas.")
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        # Rotar mano
        orden = ['izq', 'arriba', 'der', 'jugador']
        st.session_state.es_mano = orden[(orden.index(st.session_state.es_mano) + 1) % 4]
        st.session_state.estado = "INICIO"
        st.rerun()
