import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Pro - Vanesa", layout="wide")

# --- INICIALIZACIÓN ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'baraja': [],
        'descartadas': [],
        'lance_actual': None,
        'historial': "¡Mesa lista! Reparte para empezar."
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

# --- MOTOR DE CARTAS ---
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
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

def ejecutar_descarte(indices_u):
    for i in indices_u: st.session_state.descartadas.append(st.session_state.partida['jugador'][i])
    mano_u = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in indices_u]
    while len(mano_u) < 4: mano_u.append(sacar_carta())
    st.session_state.partida['jugador'] = mano_u
    
    for k in ['izq', 'arriba', 'der']:
        mano = st.session_state.partida[k]
        a_quitar = [c for c in mano if c['num'] not in [12, 1, 3, 2]]
        st.session_state.descartadas.extend(a_quitar)
        conservar = [c for c in mano if c['num'] in [12, 1, 3, 2]]
        while len(conservar) < 4: conservar.append(sacar_carta())
        st.session_state.partida[k] = conservar
    
    st.session_state.estado = "MUS"
    st.session_state.historial = "Descarte hecho. ¿Vuelve a haber Mus?"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

def dibujar_mesa(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return []
    cols = st.columns(4)
    sel = []
    for i, c in enumerate(mano):
        with cols[i]:
            fname = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", fname)
            if os.path.exists(path): st.image(path)
            else: st.button("🎴", key=f"x_{clave}_{i}")
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.checkbox("Tirar", key=f"c_{i}"): sel.append(i)
    return sel

# Mesa visual
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mesa('arriba', "PAREJA")
ci, cm, cd = st.columns([1, 1, 1])
with ci: dibujar_mesa('izq', "RIVAL IZQ")
with cd: dibujar_mesa('der', "RIVAL DER")
_, cy, _ = st.columns([1, 1, 1])
with cy: indices = dibujar_mesa('jugador', "VANESA (TÚ)", visible=True)

st.write("---")

# --- CONTROL DE FLUJO ---
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("✅ PEDIR MUS", use_container_width=True):
        # LA IA DECIDE:
        quien_corta = None
        for rival in ['izq', 'der']:
            mano_r = st.session_state.partida[rival]
            # Si tienen Rey o 3, cortan con 80% de probabilidad
            tiene_jugada = any(c['num'] in [12, 3] for c in mano_r)
            if tiene_jugada and random.random() < 0.8:
                quien_corta = "Rival Izquierdo" if rival == 'izq' else "Rival Derecho"
                break
        
        if quien_corta:
            st.session_state.estado = "JUEGO"
            st.session_state.historial = f"¡{quien_corta} CORTA el Mus! Empezamos lances."
        else:
            st.session_state.estado = "DESCARTE"
            st.session_state.historial = "Hay Mus. Elige tus descartes."
        st.rerun()
        
    if c2.button("❌ CORTO", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.session_state.historial = "Has cortado. Grande a falta."
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CONFIRMAR DESCARTE ({len(indices)})", use_container_width=True):
        ejecutar_descarte(indices)
        st.rerun()

elif st.session_state.estado == "JUEGO":
    st.markdown("<p style='color:gold; text-align:center;'>LANCES Y APUESTAS</p>", unsafe_allow_html=True)
    l_cols = st.columns(4)
    nombres_lances = ["GRANDE", "CHICA", "PARES", "JUEGO"]
    for i, lance in enumerate(nombres_lances):
        if l_cols[i].button(lance, use_container_width=True, type="primary" if st.session_state.lance_actual == lance else "secondary"):
            st.session_state.lance_actual = lance
            st.rerun()
            
    if st.session_state.lance_actual:
        st.info(f"Apostando en: {st.session_state.lance_actual}")
        a_cols = st.columns(4)
        if a_cols[0].button("PASO", use_container_width=True): st.session_state.historial = f"Pasas en {st.session_state.lance_actual}"
        if a_cols[1].button("ENVIDO", use_container_width=True): st.session_state.historial = "¡Envidas 2!"
        if a_cols[2].button("ÓRDAGO", use_container_width=True): st.session_state.historial = "¡ÓRDAGO!"
        if a_cols[3].button("QUIERO", use_container_width=True): st.session_state.historial = "¡Quieres la apuesta!"
        
    if st.button("🔄 Nueva Mano / Limpiar", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.session_state.lance_actual = None
        st.rerun()
