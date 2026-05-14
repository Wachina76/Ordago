import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Oficial Fournier", layout="wide")

# --- MOTOR DE REGLAS ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'lance_idx': 0,
        'historial': "Bienvenido al Mus. Reglamento Fournier.",
        'es_mano': 'izq'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .label-jugador { color: #FFD700; font-size: 0.8rem; text-align: center; background: rgba(0,0,0,0.6); padding: 4px; border-radius: 5px; }
    .consola-central { 
        background: rgba(0,0,0,0.9); color: #0f0; font-family: monospace; 
        padding: 20px; border-radius: 10px; border: 2px solid #FFD700; 
        text-align: center; min-height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .marcador { background: #333; color: white; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid gold; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE JUEGO ---
def calcular_valor(n):
    if n == 3: return 12 # El 3 es Rey
    if n == 2: return 1  # El 2 es As
    return n

def tiene_pares(mano):
    nums = [calcular_valor(c['num']) for c in mano]
    return len(nums) != len(set(nums))

def calcular_puntos_juego(mano):
    total = 0
    for c in mano:
        n = c['num']
        if n in [10, 11, 12, 3]: total += 10
        elif n == 2: total += 1
        else: total += n
    return total

def avanzar_lance():
    st.session_state.lance_idx += 1
    if st.session_state.lance_idx >= len(LANCES):
        st.session_state.estado = "FIN_MANO"
        st.session_state.historial = "Mano finalizada. Se cuentan los puntos en el orden del reglamento."
        return

    # Regla Fournier: Si es Pares o Juego, verificar si alguien tiene
    lance_actual = LANCES[st.session_state.lance_idx]
    if lance_actual == "PARES":
        alguien_tiene = any(tiene_pares(st.session_state.partida[k]) for k in st.session_state.partida)
        if not alguien_tiene:
            st.session_state.historial = "Nadie tiene PARES. Pasamos a JUEGO."
            avanzar_lance()
    elif lance_actual == "JUEGO/PUNTO":
        # Se juega Punto si nadie llega a 31
        pass

def repartir():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    nums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
    random.shuffle(baraja)
    st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
    st.session_state.estado = "MUS"
    st.session_state.lance_idx = 0
    st.session_state.historial = "Mano servida. ¿Hay Mus?"

# --- INTERFAZ ---
# Marcador superior
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]} piedras</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]} piedras</div>', unsafe_allow_html=True)

# Mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: 
    mano_mark = " ✋" if st.session_state.es_mano == 'arriba' else ""
    st.markdown(f'<div class="label-jugador">PAREJA{mano_mark}</div>', unsafe_allow_html=True)
    st.image(os.path.join("img", "reverso.png"), width=45)

ci, cm, cd = st.columns([1, 1.5, 1])
with ci:
    mano_mark = " ✋" if st.session_state.es_mano == 'izq' else ""
    st.markdown(f'<div class="label-jugador">RIVAL IZQ{mano_mark}</div>', unsafe_allow_html=True)
    st.image(os.path.join("img", "reverso.png"), width=45)
with cm:
    st.markdown(f'<div class="consola-central"><b>{LANCES[st.session_state.lance_idx] if st.session_state.estado == "JUEGO" else "FASE: " + st.session_state.estado}</b><br><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with cd:
    mano_mark = " ✋" if st.session_state.es_mano == 'der' else ""
    st.markdown(f'<div class="label-jugador">RIVAL DER{mano_mark}</div>', unsafe_allow_html=True)
    st.image(os.path.join("img", "reverso.png"), width=45)

_, cy, _ = st.columns([1, 1, 1])
with cy:
    mano_mark = " ✋" if st.session_state.es_mano == 'jugador' else ""
    st.markdown(f'<div class="label-jugador">VANESA (TÚ){mano_mark}</div>', unsafe_allow_html=True)
    if st.session_state.partida['jugador']:
        cols = st.columns(4)
        for i, carta in enumerate(st.session_state.partida['jugador']):
            cols[i].image(os.path.join("img", f"{str(carta['num']).zfill(2)}-{carta['palo']}.png"), width=45)

# --- BOTONES ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR (REGLAS FOURNIER)", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ PEDIR MUS", use_container_width=True):
        st.session_state.historial = "Hay mus de todos. Elige descartes."
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if col2.button("❌ CORTO", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    b1, b2, b3 = st.columns(3)
    if b1.button("PASO", use_container_width=True):
        st.session_state.historial = f"Paso en {LANCES[st.session_state.lance_idx]}."
        avanzar_lance()
        st.rerun()
    if b2.button("ENVIDO", use_container_width=True):
        # IA Responde según reglamento
        if random.random() > 0.4:
            st.session_state.historial = "¡Rival QUIERE!"
            st.session_state.puntos['nosotros'] += 0 # Se cuentan al final
        else:
            st.session_state.historial = "Rival no quiere. Te llevas 1 piedra."
            st.session_state.puntos['nosotros'] += 1
        avanzar_lance()
        st.rerun()
    if b3.button("ÓRDAGO", use_container_width=True):
        st.session_state.historial = "El rival se retira del órdago."
        st.session_state.puntos['nosotros'] += 1
        avanzar_lance()
        st.rerun()

if st.session_state.estado == "FIN_MANO":
    if st.button("🔄 RECUENTO Y SIGUIENTE MANO", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.rerun()
