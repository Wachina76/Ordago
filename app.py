import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Fournier - YO", layout="wide")

# --- REGLAS DE PUNTUACIÓN ---
def calcular_puntos_pares(mano):
    nums = [c['num'] for c in mano]
    counts = {n: nums.count(n) for n in set(nums)}
    if 4 in counts.values(): return 3  # Duples
    if 3 in counts.values(): return 2  # Medias
    if list(counts.values()).count(2) == 2: return 3  # Duples
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
        'historial': "¡Mesa lista! 31 vale 3 y Medias valen 2.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .label-jugador { color: #FFD700; font-size: 1rem; text-align: center; background: rgba(0,0,0,0.8); padding: 5px; border-radius: 5px; border: 1px solid #FFD700; margin-bottom: 10px;}
    .consola-central { background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; padding: 20px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; min-height: 160px; }
    .lance-rojo { color: #FF4B4B; font-size: 1.8rem; font-weight: bold; text-transform: uppercase; }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-size: 1.4rem; font-weight: bold;}
    /* Botones de descarte estilo 'check' */
    .stButton > button { width: 100%; }
    .btn-descarte { background-color: #FF4B4B !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA (Marcadores) ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

# --- FUNCIONES DE DIBUJO ---
def dibujar_mano(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            # Si estamos en descarte, el botón va ARRIBA de la carta para que se vea bien
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                es_tirar = i in st.session_state.seleccionados
                label = "🗑️ TIRAR" if es_tirar else "✅ OK"
                if st.button(label, key=f"des_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()
            
            img_path = os.path.join("img", f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png")
            if os.path.exists(img_path): st.image(img_path)
            else: st.info(f"{c['num']} {c['palo']}")

# --- MESA DE JUEGO ---
st.write("")
t1, t2, t3 = st.columns([1, 1, 1])
with t2: dibujar_mano('arriba', f"PAREJA ({st.session_state.nombres['arriba']})", visible=(st.session_state.estado == "REVELAR"))

r1, r2, r3 = st.columns([1, 1.5, 1])
with r1: dibujar_mano('izq', st.session_state.nombres['izq'], visible=(st.session_state.estado == "REVELAR"))
with r2:
    l_act = LANCES[st.session_state.lance_idx] if st.session_state.estado == "JUEGO" else ""
    st.markdown(f'<div class="consola-central"><div class="lance-rojo">{l_act}</div><br><b>{st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with r3: dibujar_mano('der', st.session_state.nombres['der'], visible=(st.session_state.estado == "REVELAR"))

_, y2, _ = st.columns([1, 1, 1])
with y2: dibujar_mano('jugador', "YO", visible=True)

# --- PANEL DE ACCIONES (UBICACIÓN MEJORADA) ---
st.write("---")
c_act = st.container()

with c_act:
    if st.session_state.estado == "INICIO":
        if st.button("🧧 EMPEZAR MANO", use_container_width=True, type="primary"):
            palos, nums = ['oros', 'copas', 'espadas', 'bastos'], [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
            baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
            random.shuffle(baraja)
            st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
            st.session_state.baraja = baraja[16:]; st.session_state.estado = "MUS"; st.rerun()

    elif st.session_state.estado == "MUS":
        col1, col2 = st.columns(2)
        if col1.button("✅ PEDIR MUS", use_container_width=True): st.session_state.estado = "DESCARTE"; st.rerun()
        if col2.button("❌ CORTAR", use_container_width=True): st.session_state.estado = "JUEGO"; st.rerun()

    elif st.session_state.estado == "DESCARTE":
        # Botón de confirmación prominente cerca de tu mano
        if st.button(f"♻️ CAMBIAR LAS {len(st.session_state.seleccionados)} CARTAS MARCADAS", use_container_width=True, type="primary"):
            def sacar_carta():
                if not st.session_state.baraja:
                    st.session_state.baraja = st.session_state.descartadas.copy(); random.shuffle(st.session_state.baraja)
                    st.session_state.descartadas = []
                return st.session_state.baraja.pop(0)
            
            mano_n = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in st.session_state.seleccionados]
            while len(mano_n) < 4: mano_n.append(sacar_carta())
            st.session_state.partida['jugador'] = mano_n
            # Descarte automático IA (inteligente: tiran lo que no es Rey/As/Figura)
            for k in ['izq', 'arriba', 'der']:
                m = st.session_state.partida[k]
                m_buena = [c for c in m if c['num'] in [12, 1, 3, 2, 11, 10]]
                while len(m_buena) < 4: m_buena.append(sacar_carta())
                st.session_state.partida[k] = m_buena
            st.session_state.seleccionados = []; st.session_state.estado = "MUS"; st.rerun()

    elif st.session_state.estado == "JUEGO":
        j1, j2, j3 = st.columns(3)
        if j1.button("PASO / NO TENGO", use_container_width=True):
            st.session_state.lance_idx += 1
            if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
            st.rerun()
        if j2.button("ENVIDO (2)", use_container_width=True):
            st.session_state.puntos['nosotros'] += 2 # Suma directa para test
            st.session_state.lance_idx += 1
            if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
            st.rerun()
        if j3.button("ÓRDAGO", use_container_width=True):
            st.session_state.estado = "REVELAR"; st.rerun()

    elif st.session_state.estado == "REVELAR":
        if st.button("🔄 RECOGER Y NUEVA MANO", use_container_width=True, type="primary"):
            st.session_state.estado = "INICIO"; st.session_state.lance_idx = 0; st.rerun()
