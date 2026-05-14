import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Pro - Vanesa", layout="wide")

# --- INICIALIZACIÓN ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'baraja': [],
        'descartadas': [],
        'lance_actual': None,
        'historial': "¡Mesa lista! Pulsa repartir."
    })

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 45px !important; border-radius: 4px; }
    .label-jugador { color: #FFD700; font-size: 0.7rem; text-align: center; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 5px; margin-bottom:5px;}
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px; border: 1px solid #0f0; min-height: 45px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE IA DE APUESTAS ---
def respuesta_ia_apuesta(tipo_apuesta):
    # Lógica de respuesta rápida: los rivales evalúan si aceptan tu envite
    # Basado en probabilidad simple para mantener la velocidad
    prob = random.random()
    if tipo_apuesta == "ENVIDO":
        if prob > 0.6:
            return "¡Rival dice QUIERO! (2 tantos en juego)"
        elif prob > 0.3:
            return "El rival se lo piensa... ¡y NO QUIERE! Te llevas 1 tanto."
        else:
            return "¡Rival RESUBRE! Te envida 5 más."
    elif tipo_apuesta == "ÓRDAGO":
        if prob > 0.85:
            return "¡OJO! ¡EL RIVAL QUIERE EL ÓRDAGO! Se acaba la mano."
        else:
            return "El rival se asusta... ¡NO QUIERE el Órdago!"
    return "El rival pasa."

# --- FUNCIONES DE CARTA ---
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
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

def dibujar_mesa(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
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

# Dibujo de mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mesa('arriba', "PAREJA")
ci, cm, cd = st.columns([1, 1, 1])
with ci: dibujar_mesa('izq', "RIVAL IZQ")
with cd: dibujar_mesa('der', "RIVAL DER")
_, cy, _ = st.columns([1, 1, 1])
with cy: indices = dibujar_mesa('jugador', "VANESA (TÚ)", visible=True)

st.write("---")

# --- ACCIONES ---
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("✅ PEDIR MUS", use_container_width=True):
        # IA rápida decide si corta
        corta = any(any(c['num'] in [12, 3] for c in st.session_state.partida[k]) for k in ['izq', 'der'])
        if corta and random.random() > 0.6:
            st.session_state.estado = "JUEGO"
            st.session_state.historial = "¡Rival corta! A lances."
        else:
            st.session_state.estado = "DESCARTE"
            st.session_state.historial = "Hay Mus. Descarta."
        st.rerun()
    if c2.button("❌ CORTO", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CONFIRMAR DESCARTE", use_container_width=True):
        # Lógica de descarte abreviada para velocidad
        st.session_state.estado = "MUS"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    st.markdown("<p style='color:gold; text-align:center;'> PANEL DE APUESTAS </p>", unsafe_allow_html=True)
    l_cols = st.columns(4)
    for i, l in enumerate(["GRANDE", "CHICA", "PARES", "JUEGO"]):
        if l_cols[i].button(l, use_container_width=True, type="primary" if st.session_state.lance_actual == l else "secondary"):
            st.session_state.lance_actual = l
            st.rerun()
            
    if st.session_state.lance_actual:
        a_cols = st.columns(4)
        if a_cols[0].button("PASO", use_container_width=True):
            st.session_state.historial = f"Pasas en {st.session_state.lance_actual}. El siguiente habla."
            st.rerun()
        if a_cols[1].button("ENVIDO", use_container_width=True):
            st.session_state.historial = respuesta_ia_apuesta("ENVIDO")
            st.rerun()
        if a_cols[2].button("ÓRDAGO", use_container_width=True):
            st.session_state.historial = respuesta_ia_apuesta("ÓRDAGO")
            st.rerun()
        if a_cols[3].button("QUIERO", use_container_width=True):
            st.session_state.historial = "¡Quieres! Se guardan los tantos para el final."
            st.rerun()
        
    if st.button("🔄 Nueva Mano", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.session_state.lance_actual = None
        st.rerun()
