import streamlit as st
import random
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mus Fournier Profesional", layout="wide")

# --- MOTOR DE REGLAS Y PUNTUACIÓN ---
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

# --- INICIALIZACIÓN DE ESTADO ---
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
        'historial': "¡Bienvenida! IA agresiva activada.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- LÓGICA DE BARRENO (SACAR CARTAS) ---
def sacar_carta():
    if not st.session_state.baraja:
        st.session_state.baraja = st.session_state.descartadas.copy()
        random.shuffle(st.session_state.baraja)
        st.session_state.descartadas = []
    if len(st.session_state.baraja) == 0:
        return {'num': 1, 'palo': 'oros'} # Emergencia
    return st.session_state.baraja.pop(0)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-size: 1.2rem; font-weight: bold;}
    .label-jugador { color: #FFD700; text-align: center; background: rgba(0,0,0,0.7); padding: 3px; border-radius: 5px; font-size: 0.9rem;}
    .consola { background: rgba(0,0,0,0.9); color: #0f0; font-family: monospace; padding: 15px; border: 1px solid #FFD700; text-align: center; border-radius: 10px;}
    img { border-radius: 8px; transition: transform 0.2s; }
    .stButton button { padding: 2px 5px !important; font-size: 0.8rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

# --- DIBUJAR MANOS ---
def dibujar_mano(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            # Botones de descarte pequeños
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("🗑️" if i in st.session_state.seleccionados else "✅", key=f"d_{clave}_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()
            
            img_name = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", img_name)
            if os.path.exists(path):
                st.image(path, width=80) # Tamaño controlado
            else:
                st.code(f"{c['num']} {c['palo'][:1]}")

# --- MESA ---
st.write("")
st.columns([1, 1, 1])[1].write(dibujar_mano('arriba', st.session_state.nombres['arriba'], st.session_state.estado == "REVELAR"))
c_izq, c_mid, c_der = st.columns([1, 1.2, 1])
with c_izq: dibujar_mano('izq', st.session_state.nombres['izq'], st.session_state.estado == "REVELAR")
with c_mid:
    st.markdown(f'<div class="consola"><b>{st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with c_der: dibujar_mano('der', st.session_state.nombres['der'], st.session_state.estado == "REVELAR")
st.columns([1, 1, 1])[1].write(dibujar_mano('jugador', "YO", True))

# --- ACCIONES ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR NUEVA MANO", use_container_width=True, type="primary"):
        palos, nums = ['oros', 'copas', 'espadas', 'bastos'], [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
        random.shuffle(baraja)
        st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
        st.session_state.baraja = baraja[16:]
        st.session_state.estado = "MUS"
        st.session_state.historial = "¿Pedimos mus?"
        st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ PEDIR MUS", use_container_width=True):
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if col2.button("❌ CORTAR", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CAMBIAR {len(st.session_state.seleccionados)} CARTAS", use_container_width=True, type="primary"):
        # Lógica real de cambio
        mano_actual = st.session_state.partida['jugador']
        mano_nueva = []
        for i in range(4):
            if i in st.session_state.seleccionados:
                st.session_state.descartadas.append(mano_actual[i])
                mano_nueva.append(sacar_carta())
            else:
                mano_nueva.append(mano_actual[i])
        
        st.session_state.partida['jugador'] = mano_nueva
        
        # IA también se descarta (tiran lo que no sea Rey/As)
        for k in ['izq', 'arriba', 'der']:
            m_ia = st.session_state.partida[k]
            m_n = [c for c in m_ia if c['num'] in [12, 1, 3, 2]]
            while len(m_n) < 4: m_n.append(sacar_carta())
            st.session_state.partida[k] = m_n
            
        st.session_state.seleccionados = []
        st.session_state.estado = "MUS"
        st.session_state.historial = "Cartas cambiadas. ¿Mus de nuevo?"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    b1, b2, b3 = st.columns(3)
    if b1.button("PASO", use_container_width=True):
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b2.button("ENVIDO", use_container_width=True):
        st.session_state.puntos['nosotros'] += 2
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b3.button("ÓRDAGO", use_container_width=True):
        st.session_state.estado = "REVELAR"
        st.rerun()

elif st.session_state.estado == "REVELAR":
    if st.button("🔄 RECOGER CARTAS", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.session_state.lance_idx = 0
        st.rerun()
