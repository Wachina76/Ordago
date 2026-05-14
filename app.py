import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Oficial Fournier", layout="wide")

# --- NOMBRES ALEATORIOS ---
NOMBRES_RIVALES = ["Paco", "Lola", "Curro", "Elena", "Pepe", "Marta", "Rafa", "Sonia"]

# --- MOTOR DE REGLAS ---
if 'estado' not in st.session_state:
    rivales = random.sample(NOMBRES_RIVALES, 3)
    st.session_state.update({
        'estado': "INICIO", 
        'nombres': {'izq': rivales[0], 'arriba': rivales[1], 'der': rivales[2]},
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'baraja': [],
        'descartadas': [],
        'lance_idx': 0,
        'historial': "¡Mesa lista! La IA ahora evaluará si te corta el mus.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- LÓGICA DE IA (Nivel Competitivo) ---
def ia_quiere_mus(mano):
    # La IA corta el mus si tiene algo muy bueno (ej. 2 o más figuras/reyes)
    figuras = [c for c in mano if c['num'] in [12, 11, 10, 3]]
    # Si tiene 2 figuras o más, o tiene un par grande, corta.
    if len(figuras) >= 2:
        return False
    return True

def ia_decide_apuesta(mano, lance):
    # Lógica simple de envite: si tiene cartas altas en Grande, o bajas en Chica
    nums = [c['num'] for c in mano]
    if lance == "GRANDE" and any(n in [12, 3] for n in nums):
        return "ENVIDO"
    if lance == "CHICA" and any(n in [1, 2] for n in nums):
        return "ENVIDO"
    return "PASO"

# --- FUNCIONES DE CARTA ---
def obtener_ruta_carta(carta, visible):
    if not visible:
        return os.path.join("img", "reverso.png")
    return os.path.join("img", f"{str(carta['num']).zfill(2)}-{carta['palo']}.png")

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
    st.session_state.estado = "MUS"
    st.session_state.lance_idx = 0
    st.session_state.seleccionados = []
    
    # La IA revisa si corta el mus nada más repartir
    for k in ['izq', 'arriba', 'der']:
        if not ia_quiere_mus(st.session_state.partida[k]):
            st.session_state.estado = "JUEGO"
            st.session_state.historial = f"{st.session_state.nombres[k]} ha CORTADO el mus. ¡A jugar!"
            return
    st.session_state.historial = "Todos piden mus. ¿Tú qué haces?"

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .label-jugador { color: #FFD700; font-size: 0.9rem; text-align: center; background: rgba(0,0,0,0.8); padding: 5px; border-radius: 5px; border: 1px solid #FFD700; }
    .consola-central { background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; padding: 20px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; min-height: 150px; }
    .lance-rojo { color: #FF4B4B; font-size: 1.8rem; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #444; font-size: 1.3rem;}
    </style>
    """, unsafe_allow_html=True)

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
            img_path = obtener_ruta_carta(c, visible)
            if os.path.exists(img_path): st.image(img_path, use_container_width=True)
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("TIRAR" if i in st.session_state.seleccionados else "OK", key=f"sel_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()

# Layout Mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mano('arriba', f"PAREJA ({st.session_state.nombres['arriba']})", visible=(st.session_state.estado == "REVELAR"))

ci, cm, cd = st.columns([1, 1.5, 1])
with ci: dibujar_mano('izq', st.session_state.nombres['izq'], visible=(st.session_state.estado == "REVELAR"))
with cm:
    l_act = LANCES[st.session_state.lance_idx] if st.session_state.estado == "JUEGO" else ""
    st.markdown(f'<div class="consola-central"><div class="lance-rojo">{l_act}</div><b>{st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with cd: dibujar_mano('der', st.session_state.nombres['der'], visible=(st.session_state.estado == "REVELAR"))

_, cy, _ = st.columns([1, 1, 1])
with cy: dibujar_mano('jugador', "YO (MANO)" if st.session_state.es_mano == 'jugador' else "YO", visible=True)

# --- BOTONES DE CONTROL ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 EMPEZAR PARTIDA", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ PEDIR MUS", use_container_width=True):
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if col2.button("❌ CORTAR", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.session_state.historial = "Has cortado el mus. Empezamos la Grande."
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CONFIRMAR DESCARTE", use_container_width=True):
        # Tu descarte
        nuevas = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in st.session_state.seleccionados]
        for i in st.session_state.seleccionados: st.session_state.descartadas.append(st.session_state.partida['jugador'][i])
        while len(nuevas) < 4: nuevas.append(sacar_carta())
        st.session_state.partida['jugador'] = nuevas
        # Descarte IA y ver si vuelven a querer mus
        for k in ['izq', 'arriba', 'der']:
            m = st.session_state.partida[k]
            cons = [c for c in m if c['num'] in [12, 1, 3, 2]]
            while len(cons) < 4: cons.append(sacar_carta())
            st.session_state.partida[k] = cons
        st.session_state.seleccionados = []
        # ¿Vuelven a querer mus?
        for k in ['izq', 'arriba', 'der']:
            if not ia_quiere_mus(st.session_state.partida[k]):
                st.session_state.estado = "JUEGO"
                st.session_state.historial = f"{st.session_state.nombres[k]} corta el mus tras el descarte."
                st.rerun()
        st.session_state.estado = "MUS"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("PASO", use_container_width=True):
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b2.button("ENVIDO (2)", use_container_width=True):
        if random.random() > 0.5:
            st.session_state.historial = "¡Rival QUIERE el envite!"; st.session_state.puntos['nosotros'] += 2
        else:
            st.session_state.historial = "Rival se achica. +1 piedra"; st.session_state.puntos['nosotros'] += 1
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b3.button("ÓRDAGO", use_container_width=True):
        if random.random() > 0.8: # IA muy valiente
            st.session_state.historial = "¡RIVAL QUIERE EL ÓRDAGO! Se acaba el chico."
            st.session_state.estado = "REVELAR"
        else:
            st.session_state.historial = "Rival no quiere órdago. +1 para ti."
            st.session_state.puntos['nosotros'] += 1
            st.session_state.lance_idx += 1
            if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

if st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        orden = ['jugador', 'izq', 'arriba', 'der']
        st.session_state.es_mano = orden[(orden.index(st.session_state.es_mano) + 1) % 4]
        st.session_state.estado = "INICIO"
        st.rerun()
