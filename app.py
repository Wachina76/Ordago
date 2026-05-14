import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Fournier - Vanesa", layout="wide")

# --- MOTOR DE REGLAS ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'apuestas': {'GRANDE': 0, 'CHICA': 0, 'PARES': 0, 'JUEGO/PUNTO': 0},
        'ganadores_lance': {},
        'baraja': [],
        'descartadas': [],
        'lance_idx': 0,
        'historial': "Sentido de la mano: Jugador -> Izquierda -> Pareja -> Derecha.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- LÓGICA DE EVALUACIÓN (REGLAMENTO FOURNIER) ---
def obtener_valor_carta(n):
    if n == 3: return 13 # El 3 es Rey (valor máximo)
    if n == 2: return 1  # El 2 es As (valor mínimo)
    return n

def evaluar_grande(mano):
    valores = sorted([obtener_valor_carta(c['num']) for c in mano], reverse=True)
    return valores

def evaluar_chica(mano):
    valores = sorted([obtener_valor_carta(c['num']) for c in mano])
    return valores

def recuento_final():
    # Simplificación de recuento para el flujo rápido
    nosotros_p = st.session_state.puntos['nosotros']
    ellos_p = st.session_state.puntos['ellos']
    
    resumen = "RECUENTO FINAL: "
    # Evaluación Grande
    v_jug = evaluar_grande(st.session_state.partida['jugador'])
    v_izq = evaluar_grande(st.session_state.partida['izq'])
    
    if v_jug > v_izq:
        st.session_state.puntos['nosotros'] += 1
        resumen += " | Ganáis Grande (+1)"
    else:
        st.session_state.puntos['ellos'] += 1
        resumen += " | Ellos ganan Grande (+1)"
        
    st.session_state.historial = resumen

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .label-jugador { color: #FFD700; font-size: 0.8rem; text-align: center; background: rgba(0,0,0,0.6); padding: 4px; border-radius: 5px; margin-bottom: 5px;}
    .consola-central { background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; padding: 20px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; min-height: 140px; }
    .lance-rojo { color: #FF4B4B; font-size: 1.6rem; font-weight: bold; text-transform: uppercase; text-shadow: 2px 2px #000; }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-size: 1.3rem;}
    </style>
    """, unsafe_allow_html=True)

# --- INTERFAZ ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOS: {st.session_state.puntos["nosotros"]} / 40</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]} / 40</div>', unsafe_allow_html=True)

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

# Mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mano('arriba', "PAREJA", visible=(st.session_state.estado == "REVELAR"))
ci, cm, cd = st.columns([1, 1.5, 1])
with ci: dibujar_mano('izq', "RIVAL IZQ", visible=(st.session_state.estado == "REVELAR"))
with cm:
    l_act = LANCES[st.session_state.lance_idx] if st.session_state.estado == "JUEGO" else ""
    st.markdown(f'<div class="consola-central"><div class="lance-rojo">{l_act}</div><b>{st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with cd: dibujar_mano('der', "RIVAL DER", visible=(st.session_state.estado == "REVELAR"))
_, cy, _ = st.columns([1, 1, 1])
with cy: indices_descarte = dibujar_mano('jugador', "VANESA (TÚ)", visible=True)

# --- BOTONES Y LOGICA ---
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        palos = ['oros', 'copas', 'espadas', 'bastos']
        nums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
        random.shuffle(baraja)
        st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
        st.session_state.baraja = baraja[16:]; st.session_state.estado = "MUS"
        st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ MUS", use_container_width=True): st.session_state.estado = "DESCARTE"; st.rerun()
    if col2.button("❌ CORTAR", use_container_width=True): st.session_state.estado = "JUEGO"; st.rerun()

elif st.session_state.estado == "JUEGO":
    b1, b2, b3 = st.columns(3)
    if b1.button("PASO", use_container_width=True):
        st.session_state.historial = "Pasas. Nadie envida."
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4:
            st.session_state.estado = "REVELAR"
            recuento_final()
        st.rerun()
    if b2.button("ENVIDO (2)", use_container_width=True):
        st.session_state.puntos['nosotros'] += 2
        st.session_state.historial = "¡Rival QUIERE! (+2 para el final)"
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4:
            st.session_state.estado = "REVELAR"
            recuento_final()
        st.rerun()

if st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        orden = ['jugador', 'izq', 'arriba', 'der']
        idx = orden.index(st.session_state.es_mano)
        st.session_state.es_mano = orden[(idx + 1) % 4]
        st.session_state.estado = "INICIO"
        st.session_state.lance_idx = 0
        st.rerun()
