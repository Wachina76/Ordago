import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Oficial Fournier", layout="wide")

# --- REGLAS DE PUNTUACIÓN REALES ---
def calcular_puntos_pares(mano):
    nums = [c['num'] for c in mano]
    counts = {n: nums.count(n) for n in set(nums)}
    if 4 in counts.values(): return 3 # Duples
    if 3 in counts.values(): return 2 # Medias
    if list(counts.values()).count(2) == 2: return 3 # Duples (dos parejas)
    if 2 in counts.values(): return 1 # Par
    return 0

def calcular_puntos_juego(mano):
    # En el Mus, las figuras valen 10, el resto su valor
    suma = sum([min(c['num'], 10) for c in mano])
    if suma == 31: return 3
    if suma > 30: return 2
    return 0

# --- MOTOR DEL JUEGO ---
if 'estado' not in st.session_state:
    rivales = random.sample(["Paco", "Lola", "Curro", "Elena"], 3)
    st.session_state.update({
        'estado': "INICIO", 
        'nombres': {'izq': rivales[0], 'arriba': rivales[1], 'der': rivales[2]},
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'baraja': [],
        'descartadas': [],
        'lance_idx': 0,
        'historial': "¡Mesa lista! 31 vale 3 y Medias valen 2.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- LÓGICA DE RECUENTO AUTOMÁTICO ---
def realizar_recuento_final():
    resumen = "RECUENTO: "
    
    # Recuento de Pares
    p_yo = calcular_puntos_pares(st.session_state.partida['jugador'])
    p_izq = calcular_puntos_pares(st.session_state.partida['izq'])
    
    if p_yo > 0:
        st.session_state.puntos['nosotros'] += p_yo
        resumen += f"| Mis Pares (+{p_yo}) "
    if p_izq > 0:
        st.session_state.puntos['ellos'] += p_izq
        resumen += f"| Sus Pares (+{p_izq}) "
        
    # Recuento de Juego
    j_yo = calcular_puntos_juego(st.session_state.partida['jugador'])
    j_izq = calcular_puntos_juego(st.session_state.partida['izq'])
    
    if j_yo > 0:
        st.session_state.puntos['nosotros'] += j_yo
        resumen += f"| Mi Juego (+{j_yo}) "
    if j_izq > 0:
        st.session_state.puntos['ellos'] += j_izq
        resumen += f"| Su Juego (+{j_izq}) "
        
    st.session_state.historial = resumen

# --- INTERFAZ ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .label-jugador { color: #FFD700; font-size: 0.9rem; text-align: center; background: rgba(0,0,0,0.8); padding: 5px; border-radius: 5px; border: 1px solid #FFD700; }
    .consola-central { background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; padding: 20px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; min-height: 160px; }
    .lance-rojo { color: #FF4B4B; font-size: 1.8rem; font-weight: bold; text-transform: uppercase; }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-size: 1.3rem;}
    </style>
    """, unsafe_allow_html=True)

m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            img_path = os.path.join("img", f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png")
            if os.path.exists(img_path): st.image(img_path)
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("TIRAR" if i in st.session_state.seleccionados else "OK", key=f"s_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()

# Layout
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mano('arriba', f"PAREJA ({st.session_state.nombres['arriba']})", visible=(st.session_state.estado == "REVELAR"))
ci, cm, cd = st.columns([1, 1.5, 1])
with ci: dibujar_mano('izq', st.session_state.nombres['izq'], visible=(st.session_state.estado == "REVELAR"))
with cm:
    l_act = LANCES[st.session_state.lance_idx] if st.session_state.estado == "JUEGO" else ""
    st.markdown(f'<div class="consola-central"><div class="lance-rojo">{l_act}</div><b>{st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with cd: dibujar_mano('der', st.session_state.nombres['der'], visible=(st.session_state.estado == "REVELAR"))
_, cy, _ = st.columns([1, 1, 1])
with cy: dibujar_mano('jugador', "YO", visible=True)

# --- BOTONES ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        palos, nums = ['oros', 'copas', 'espadas', 'bastos'], [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
        random.shuffle(baraja)
        st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
        st.session_state.baraja = baraja[16:]; st.session_state.estado = "MUS"; st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("✅ MUS", use_container_width=True): st.session_state.estado = "DESCARTE"; st.rerun()
    if c2.button("❌ CORTAR", use_container_width=True): st.session_state.estado = "JUEGO"; st.rerun()

elif st.session_state.estado == "JUEGO":
    col1, col2, col3 = st.columns(3)
    if col1.button("PASO / NO TENGO", use_container_width=True):
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4:
            st.session_state.estado = "REVELAR"
            realizar_recuento_final()
        st.rerun()
    if col2.button("ENVIDO (2)", use_container_width=True):
        st.session_state.puntos['nosotros'] += 2 # Simplificado para test
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4:
            st.session_state.estado = "REVELAR"
            realizar_recuento_final()
        st.rerun()
    if col3.button("ÓRDAGO", use_container_width=True):
        st.session_state.estado = "REVELAR"
        realizar_recuento_final()
        st.rerun()

elif st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        st.session_state.estado = "INICIO"; st.rerun()
