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
        'seleccionados': [], # Para el descarte por clic
        'baraja': [],
        'descartadas': [],
        'lance_idx': 0,
        'historial': "Pulsa sobre las cartas para descartarlas.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- CSS MEJORADO (Efectos de selección) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .label-jugador { color: #FFD700; font-size: 0.8rem; text-align: center; background: rgba(0,0,0,0.6); padding: 4px; border-radius: 5px; margin-bottom: 5px;}
    .consola-central { background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; padding: 20px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; min-height: 140px; }
    .lance-rojo { color: #FF4B4B; font-size: 1.6rem; font-weight: bold; text-transform: uppercase; text-shadow: 2px 2px #000; }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-size: 1.3rem;}
    /* Estilo para carta seleccionada */
    .carta-sel { border: 3px solid #FF4B4B !important; border-radius: 8px; transform: translateY(-10px); transition: 0.2s; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES ---
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
    st.session_state.seleccionados = []
    st.session_state.historial = "¿Hay Mus?"

# --- INTERFAZ ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]} / 40</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]} / 40</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False):
    mano_mark = " ✋" if st.session_state.es_mano == clave else ""
    st.markdown(f'<div class="label-jugador">{titulo}{mano_mark}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            fname = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            # Si estamos en descarte, las cartas son botones
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                label = "✅" if i in st.session_state.seleccionados else "🎴"
                if st.button(label, key=f"btn_{i}", use_container_width=True):
                    if i in st.session_state.seleccionados:
                        st.session_state.seleccionados.remove(i)
                    else:
                        st.session_state.seleccionados.append(i)
                    st.rerun()
            
            # Mostrar la imagen de la carta
            path = os.path.join("img", fname)
            estilo = 'class="carta-sel"' if (clave == 'jugador' and i in st.session_state.seleccionados) else ""
            if os.path.exists(path):
                st.markdown(f'<img src="f/{path}" {estilo} style="width:100%">', unsafe_allow_html=True)
            else:
                st.write(f"{c['num']} {c['palo']}")

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
with cy: dibujar_mano('jugador', "VANESA (TÚ)", visible=True)

# --- LÓGICA DE BOTONES CENTRALES ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR MANO", use_container_width=True):
        repartir()
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
    if st.button(f"♻️ CONFIRMAR DESCARTE ({len(st.session_state.seleccionados)})", use_container_width=True):
        # Procesar descarte
        nuevas = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in st.session_state.seleccionados]
        for i in st.session_state.seleccionados: st.session_state.descartadas.append(st.session_state.partida['jugador'][i])
        while len(nuevas) < 4: nuevas.append(sacar_carta())
        st.session_state.partida['jugador'] = nuevas
        
        # IA también descarta
        for k in ['izq', 'arriba', 'der']:
            m = st.session_state.partida[k]
            cons = [c for c in m if c['num'] in [12, 1, 3, 2]]
            while len(cons) < 4: cons.append(sacar_carta())
            st.session_state.partida[k] = cons
        
        st.session_state.seleccionados = []
        st.session_state.estado = "MUS"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    b1, b2, b3 = st.columns(3)
    if b1.button("PASO", use_container_width=True):
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b2.button("ENVIDO (2)", use_container_width=True):
        st.session_state.puntos['nosotros'] += 2
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

if st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        # ROTACIÓN HORARIA: Jugador -> Izq -> Arriba -> Der
        orden = ['jugador', 'izq', 'arriba', 'der']
        idx = orden.index(st.session_state.es_mano)
        st.session_state.es_mano = orden[(idx + 1) % 4]
        st.session_state.estado = "INICIO"
        st.rerun()
