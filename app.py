import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Oficial Fournier", layout="wide")

# --- MOTOR DE REGLAS ---
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
        'historial': "¡Mesa lista! Pulsa Repartir para empezar.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- FUNCIONES AUXILIARES ---
def sacar_carta():
    if not st.session_state.baraja:
        st.session_state.baraja = st.session_state.descartadas.copy()
        random.shuffle(st.session_state.baraja)
        st.session_state.descartadas = []
    return st.session_state.baraja.pop(0)

def repartir():
    palos, nums = ['oros', 'copas', 'espadas', 'bastos'], [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
    random.shuffle(baraja)
    st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
    st.session_state.baraja = baraja[16:]
    st.session_state.estado = "MUS"
    st.session_state.lance_idx = 0
    st.session_state.seleccionados = []
    st.session_state.historial = "¿Hay Mus?"

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .label-jugador { color: #FFD700; font-size: 0.9rem; text-align: center; background: rgba(0,0,0,0.8); padding: 5px; border-radius: 5px; border: 1px solid #FFD700; }
    .consola-central { background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; padding: 20px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; min-height: 160px; }
    .lance-rojo { color: #FF4B4B; font-size: 1.8rem; font-weight: bold; text-transform: uppercase; }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-size: 1.3rem;}
    .stButton button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFAZ ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False):
    mano_mark = " ✋" if st.session_state.es_mano == clave else ""
    st.markdown(f'<div class="label-jugador">{titulo}{mano_mark}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            img_name = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", img_name)
            if os.path.exists(path): st.image(path)
            else: st.button(f"{c['num']} {c['palo']}", key=f"t_{clave}_{i}")
            
            # BOTONES DE DESCARTAR (Solo visibles en fase DESCARTE para el jugador)
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                label = "🗑️ TIRAR" if i in st.session_state.seleccionados else "✅ QUEDAR"
                if st.button(label, key=f"btn_sel_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()

# Mesa
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

# --- BOTÓN DE CONFIRMACIÓN DE DESCARTE ---
if st.session_state.estado == "DESCARTE":
    st.write("---")
    if st.button(f"♻️ CAMBIAR LAS {len(st.session_state.seleccionados)} CARTAS SELECCIONADAS", use_container_width=True, type="primary"):
        # Procesar descarte YO
        mano_nueva = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in st.session_state.seleccionados]
        for i in st.session_state.seleccionados: st.session_state.descartadas.append(st.session_state.partida['jugador'][i])
        while len(mano_nueva) < 4: mano_nueva.append(sacar_carta())
        st.session_state.partida['jugador'] = mano_nueva
        
        # Procesar descarte IA (siempre tiran lo que no sea Rey/As)
        for k in ['izq', 'arriba', 'der']:
            m = st.session_state.partida[k]
            bueno = [c for c in m if c['num'] in [12, 1, 3, 2]]
            while len(bueno) < 4: bueno.append(sacar_carta())
            st.session_state.partida[k] = bueno
            
        st.session_state.seleccionados = []
        st.session_state.estado = "MUS" # Vuelve a preguntar Mus
        st.session_state.historial = "Cartas cambiadas. ¿Hay mus otra vez?"
        st.rerun()

# --- BOTONES DE CONTROL GENERAL ---
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
    if col2.button("❌ CORTAR / JUGAR", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    col1, col2, col3 = st.columns(3)
    if col1.button("PASO / NO TENGO", use_container_width=True):
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if col2.button("ENVIDO (2)", use_container_width=True):
        if random.random() > 0.5: st.session_state.puntos['nosotros'] += 2
        else: st.session_state.puntos['nosotros'] += 1
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if col3.button("ÓRDAGO", use_container_width=True):
        st.session_state.estado = "REVELAR"
        st.rerun()

elif st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        orden = ['jugador', 'izq', 'arriba', 'der']
        st.session_state.es_mano = orden[(orden.index(st.session_state.es_mano) + 1) % 4]
        st.session_state.estado = "INICIO"
        st.rerun()
