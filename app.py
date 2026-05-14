import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Profesional - Luis", layout="centered")

# --- REGLAS DE PUNTUACIÓN ---
def calcular_puntos_pares(mano):
    nums = [c['num'] for c in mano]
    counts = {n: nums.count(n) for n in set(nums)}
    if 4 in counts.values(): return 3  # Duples
    if 3 in counts.values(): return 2  # Medias
    if list(counts.values()).count(2) == 2: return 3 # Duples
    if 2 in counts.values(): return 1  # Par
    return 0

def calcular_puntos_juego(mano):
    suma = sum([min(c['num'], 10) for c in mano])
    if suma == 31: return 3
    if suma > 30: return 2
    return 0

# --- INICIALIZACIÓN ---
if 'estado' not in st.session_state:
    rivales = random.sample(["Paco", "Lola", "Curro", "Elena", "Pepe", "Marta"], 3)
    st.session_state.update({
        'estado': "INICIO", 
        'nombres': {'izq': rivales[0], 'arriba': rivales[1], 'der': rivales[2]},
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'baraja': [],
        'descartadas': [],
        'lance_idx': 0,
        'historial': "Mesa compacta lista. ¡A por ellos, Luis!",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

def sacar_carta():
    if not st.session_state.baraja:
        st.session_state.baraja = st.session_state.descartadas.copy()
        random.shuffle(st.session_state.baraja)
        st.session_state.descartadas = []
    return st.session_state.baraja.pop(0) if st.session_state.baraja else {'num': 1, 'palo': 'oros'}

def ia_evalua_envite(mano, lance, fuerza_necesaria=2):
    nums = [c['num'] for c in mano]
    objetivos = [12, 3] if lance == "GRANDE" else [1, 2]
    fuerza = sum(1 for n in nums if n in objetivos)
    return fuerza >= fuerza_necesaria

# --- CSS PARA COMPACTAR MESA ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .marcador { background: #222; color: gold; padding: 5px; border-radius: 8px; text-align: center; border: 1px solid #444; font-size: 1.1rem; font-weight: bold;}
    .label-jugador { color: #FFD700; text-align: center; background: rgba(0,0,0,0.7); padding: 2px; border-radius: 4px; font-size: 0.8rem; margin-bottom: 2px;}
    .consola { background: rgba(0,0,0,0.9); color: #0f0; font-family: monospace; padding: 8px; border: 1px solid #FFD700; text-align: center; border-radius: 8px; font-size: 0.9rem;}
    [data-testid="column"] { padding: 0px 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False, escala=60):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("🗑️" if i in st.session_state.seleccionados else "✅", key=f"d_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()
            img = os.path.join("img", f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png")
            if os.path.exists(img): st.image(img, width=escala)
            else: st.write(f"{c['num']}{c['palo'][0]}")

# --- MESA COMPACTA ---
_, center_top, _ = st.columns([1, 2, 1])
with center_top:
    dibujar_mano('arriba', f"COMPAÑERO ({st.session_state.nombres['arriba']})", st.session_state.estado == "REVELAR", escala=50)

c_izq, c_mid, c_der = st.columns([1, 2, 1])
with c_izq: dibujar_mano('izq', st.session_state.nombres['izq'], st.session_state.estado == "REVELAR", escala=50)
with c_mid:
    st.markdown(f'<div class="consola"><b>{st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with c_der: dibujar_mano('der', st.session_state.nombres['der'], st.session_state.estado == "REVELAR", escala=50)

_, center_bot, _ = st.columns([1, 2, 1])
with center_bot:
    dibujar_mano('jugador', "LUIS (YO)", True, escala=70)

# --- ACCIONES ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True, type="primary"):
        palos, nums = ['oros', 'copas', 'espadas', 'bastos'], [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]; random.shuffle(baraja)
        st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
        st.session_state.baraja = baraja[16:]; st.session_state.estado = "MUS"; st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ PEDIR MUS", use_container_width=True): st.session_state.estado = "DESCARTE"; st.rerun()
    if col2.button("❌ CORTAR", use_container_width=True): st.session_state.estado = "JUEGO"; st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CAMBIAR {len(st.session_state.seleccionados)} CARTAS", use_container_width=True, type="primary"):
        st.session_state.partida['jugador'] = [sacar_carta() if i in st.session_state.seleccionados else c for i, c in enumerate(st.session_state.partida['jugador'])]
        for k in ['izq', 'arriba', 'der']:
            st.session_state.partida[k] = [c if c['num'] in [12, 1, 3, 2] else sacar_carta() for c in st.session_state.partida[k]]
        st.session_state.seleccionados = []; st.session_state.estado = "MUS"; st.rerun()

elif st.session_state.estado == "JUEGO":
    lance = LANCES[st.session_state.lance_idx]
    b1, b2, b3 = st.columns(3)
    if b1.button("PASO", use_container_width=True):
        if ia_evalua_envite(st.session_state.partida['izq'], lance, 1): st.session_state.puntos['ellos'] += 1
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b2.button("ENVIDO (2)", use_container_width=True):
        if ia_evalua_envite(st.session_state.partida['izq'], lance, 2): st.session_state.puntos['nosotros'] += 2
        else: st.session_state.puntos['nosotros'] += 1
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b3.button("ÓRDAGO", use_container_width=True):
        if ia_evalua_envite(st.session_state.partida['izq'], lance, 3): st.session_state.estado = "REVELAR"
        else: st.session_state.puntos['nosotros'] += 1; st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

elif st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        st.session_state.estado = "INICIO"; st.session_state.lance_idx = 0; st.rerun()
