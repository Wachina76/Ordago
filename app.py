import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Pro - Vanesa", layout="wide")

# --- MOTOR LÓGICO ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'baraja': [],
        'lance_actual': None,
        'historial': "¡Mesa lista para la partida!"
    })

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 45px !important; border-radius: 4px; }
    .label-jugador { color: #FFD700; font-size: 0.7rem; text-align: center; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 5px; margin-bottom:5px;}
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px; border: 1px solid #0f0; min-height: 45px; margin-bottom: 10px;}
    div[data-testid="stCheckbox"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE JUEGO ---
def repartir():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    nums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
    random.shuffle(baraja)
    st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
    st.session_state.baraja = baraja[16:]
    st.session_state.estado = "MUS"
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

def ejecutar_descarte_ia_y_usuario(indices_usuario):
    # Descarte Usuario
    mano_u = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in indices_usuario]
    while len(mano_u) < 4: mano_u.append(st.session_state.baraja.pop(0))
    st.session_state.partida['jugador'] = mano_u
    
    # Descarte Automático IA (Rival Izq, Pareja, Rival Der)
    for k in ['izq', 'arriba', 'der']:
        mano = st.session_state.partida[k]
        # La IA se queda con Reyes (12), Treses (3), Ases (1) y Doses (2)
        conservar = [c for c in mano if c['num'] in [12, 1, 3, 2]]
        while len(conservar) < 4: conservar.append(st.session_state.baraja.pop(0))
        st.session_state.partida[k] = conservar
    
    st.session_state.estado = "MUS"
    st.session_state.historial = "Descarte completado. ¿Vuelve a haber Mus?"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return []
    cols = st.columns(4)
    sel = []
    for i, c in enumerate(mano):
        with cols[i]:
            img_name = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", img_name)
            if os.path.exists(path): st.image(path)
            else: st.button("🎴", key=f"btn_{clave}_{i}")
            
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.checkbox("Tirar", key=f"chk_{i}"): sel.append(i)
    return sel

# Mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_mano('arriba', "PAREJA")
ci, cm, cd = st.columns([1, 1, 1])
with ci: dibujar_mano('izq', "RIVAL IZQ")
with cd: dibujar_mano('der', "RIVAL DER")
_, cy, _ = st.columns([1, 1, 1])
with cy: indices_desc = dibujar_mano('jugador', "VANESA (TÚ)", visible=True)

# --- BOTONES ---
st.write("---")

if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        repartir()
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("✅ PEDIR MUS", use_container_width=True):
        # IA decide si acepta Mus (probabilidad alta si no tienen jugada de cara)
        corta = any(any(c['num'] == 12 for c in st.session_state.partida[k]) for k in ['izq', 'der'])
        if corta and random.random() > 0.7:
            st.session_state.estado = "JUEGO"
            st.session_state.historial = "¡Rival CORTA el Mus! Vamos a los lances."
        else:
            st.session_state.estado = "DESCARTE"
            st.session_state.historial = "Hay Mus. Selecciona cartas para descartar."
        st.rerun()
    if c2.button("❌ CORTAR", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.session_state.historial = "Has cortado. Empezamos con la GRANDE."
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ DESCARTAR SELECCIONADAS ({len(indices_desc)})", use_container_width=True):
        ejecutar_descarte_ia_y_usuario(indices_desc)
        st.rerun()

elif st.session_state.estado == "JUEGO":
    cols_l = st.columns(4)
    lances = ["GRANDE", "CHICA", "PARES", "JUEGO"]
    for i, l in enumerate(lances):
        if cols_l[i].button(l, use_container_width=True, type="primary" if st.session_state.lance_actual == l else "secondary"):
            st.session_state.lance_actual = l
            st.rerun()

    if st.session_state.lance_actual:
        st.write(f"Apuestas para {st.session_state.lance_actual}:")
        b1, b2, b3, b4 = st.columns(4)
        b1.button("PASO")
        b2.button("ENVIDO")
        b3.button("ÓRDAGO")
        b4.button("QUIERO")
        
    if st.button("🔄 Nueva Mano", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.session_state.lance_actual = None
        st.rerun()
