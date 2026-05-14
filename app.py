import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Oficial Fournier", layout="wide")

# --- NOMBRES RIVALES ---
if 'nombres' not in st.session_state:
    rivales = random.sample(["Paco", "Lola", "Curro", "Elena", "Pepe", "Marta"], 3)
    st.session_state.nombres = {'izq': rivales[0], 'arriba': rivales[1], 'der': rivales[2]}

# --- MOTOR DE REGLAS ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'baraja': [],
        'descartadas': [],
        'lance_idx': 0,
        'historial': "¡Mesa lista!",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- LÓGICA DE PUNTUACIÓN ---
def calcular_valor_mus(n):
    if n == 3: return 12 # Rey
    if n == 2: return 1  # As
    return n

def tiene_pares(mano):
    nums = [c['num'] for c in mano]
    return len(set(nums)) < 4

def calcular_puntos_juego(mano):
    # Figuras valen 10, resto su valor
    suma = sum([min(c['num'], 10) for c in mano])
    return suma if suma >= 31 else 0

def evaluar_lances_ia():
    # Esta función simula que la IA suma sus puntos al final
    # Por ahora sumamos 1-2 puntos aleatorios para los rivales para que el marcador se mueva
    if random.random() > 0.6:
        p = random.randint(1, 3)
        st.session_state.puntos['ellos'] += p
        return f" | Los rivales suman {p} tantos de recuento."
    return ""

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

# Marcadores
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
            img = os.path.join("img", f"{str(c['num']).zfill(2)}-{c['palo']}.png") if visible else os.path.join("img", "reverso.png")
            if os.path.exists(img): st.image(img)
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("TIRAR" if i in st.session_state.seleccionados else "OK", key=f"sel_{i}"):
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

# --- BOTONES ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        palos, nums = ['oros', 'copas', 'espadas', 'bastos'], [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
        random.shuffle(baraja)
        st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
        st.session_state.baraja = baraja[16:]; st.session_state.estado = "MUS"; st.rerun()

elif st.session_state.estado == "JUEGO":
    lance = LANCES[st.session_state.lance_idx]
    b1, b2, b3, b4 = st.columns(4)
    
    if b1.button("PASO / NO TENGO", use_container_width=True):
        # Si pasas, la IA puede puntuar
        msg_extra = ""
        if random.random() > 0.7:
            st.session_state.puntos['ellos'] += 1
            msg_extra = " | Ellos puntúan el lance."
        st.session_state.historial = f"Pasas en {lance}.{msg_extra}"
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

    if b2.button("ENVIDO (2)", use_container_width=True):
        if random.random() > 0.5:
            st.session_state.puntos['nosotros'] += 2
            st.session_state.historial = "¡Quieren! Sumas 2 piedras."
        else:
            st.session_state.puntos['nosotros'] += 1
            st.session_state.historial = "No quieren. Sumas 1 piedra."
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

    if b3.button("ÓRDAGO", use_container_width=True):
        if random.random() > 0.9: 
            st.session_state.historial = "¡ACEPTAN EL ÓRDAGO! Se ve todo."
            st.session_state.estado = "REVELAR"
        else:
            st.session_state.puntos['nosotros'] += 1
            st.session_state.historial = "No quieren órdago. +1 punto."
            st.session_state.lance_idx += 1
            if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("✅ MUS", use_container_width=True): st.session_state.estado = "DESCARTE"; st.rerun()
    if c2.button("❌ CORTO", use_container_width=True): st.session_state.estado = "JUEGO"; st.rerun()

elif st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        orden = ['jugador', 'izq', 'arriba', 'der']
        st.session_state.es_mano = orden[(orden.index(st.session_state.es_mano) + 1) % 4]
        st.session_state.estado = "INICIO"; st.session_state.lance_idx = 0; st.rerun()
