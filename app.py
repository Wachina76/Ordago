import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Pro - Lances", layout="wide")

# --- MOTOR LÓGICO ---
def crear_baraja_mus():
    palos = ['oros', 'copas', 'espadas', 'bastos']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'baraja': [],
        'historial': "¡Mesa lista! Pulsa repartir."
    })

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    [data-testid="stImage"] img { width: 48px !important; border-radius: 4px; }
    .label-jugador { color: #FFD700; font-size: 0.75rem; text-align: center; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 5px; margin-bottom:5px;}
    .consola { background: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px; border: 1px solid #0f0; margin-bottom: 15px; min-height: 40px;}
    div[data-testid="stCheckbox"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE JUEGO ---
def repartir_inicial():
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.partida = {
        'jugador': baraja[0:4], 'izq': baraja[4:8], 
        'arriba': baraja[8:12], 'der': baraja[12:16]
    }
    st.session_state.baraja = baraja[16:]
    st.session_state.estado = "MUS"
    st.session_state.historial = "Cartas repartidas. ¿Hay Mus?"

def ejecutar_descarte(indices_a_quitar):
    # Descarte del jugador
    mano_p = [c for i, c in enumerate(st.session_state.partida['jugador']) if i not in indices_a_quitar]
    while len(mano_p) < 4: mano_p.append(st.session_state.baraja.pop(0))
    st.session_state.partida['jugador'] = mano_p

    # Descarte IA (muy rápido)
    for k in ['izq', 'der', 'arriba']:
        mano = st.session_state.partida[k]
        nueva = [c for c in mano if c['num'] in [12, 1, 3, 2]]
        while len(nueva) < 4: nueva.append(st.session_state.baraja.pop(0))
        st.session_state.partida[k] = nueva

    st.session_state.estado = "MUS"
    st.session_state.historial = "Descarte hecho. ¿Vuelve a haber Mus?"

# --- INTERFAZ ---
st.markdown(f'<div class="consola">> {st.session_state.historial}</div>', unsafe_allow_html=True)

def dibujar_jugador(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return []
    cols = st.columns(4)
    check_indices = []
    for i, c in enumerate(mano):
        with cols[i]:
            fname = f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png"
            path = os.path.join("img", fname)
            if os.path.exists(path): st.image(path)
            else: st.button("🎴", key=f"err_{clave}_{i}")
            
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.checkbox("Tirar", key=f"t_{i}"): check_indices.append(i)
    return check_indices

# Mesa
c1, c2, c3 = st.columns([1, 1, 1])
with c2: dibujar_jugador('arriba', "PAREJA")

ci, cm, cd = st.columns([1, 1, 1])
with ci: dibujar_jugador('izq', "RIVAL IZQ")
with cd: dibujar_jugador('der', "RIVAL DER")

_, cy, _ = st.columns([1, 1, 1])
with cy: indices = dibujar_jugador('jugador', "VANESA (TÚ)", visible=True)

# --- LÓGICA DE BOTONES ---
st.write("---")

if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR MANO", use_container_width=True):
        repartir_inicial()
        st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ PEDIR MUS", use_container_width=True):
        # La IA decide si corta o da Mus
        corta_ia = any(any(c['num'] == 12 for c in st.session_state.partida[k]) for k in ['izq','der'])
        if corta_ia and random.random() > 0.6:
            st.session_state.estado = "JUEGO"
            st.session_state.historial = "¡Rival corta el mus! A jugar Grande."
        else:
            st.session_state.estado = "DESCARTE"
            st.session_state.historial = "Hay mus. Elige qué cartas tirar."
        st.rerun()
    if col2.button("❌ CORTO (NO HAY MUS)", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.session_state.historial = "¡Cortado! Empieza la Grande."
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CONFIRMAR DESCARTE ({len(indices)})", use_container_width=True):
        ejecutar_descarte(indices)
        st.rerun()

elif st.session_state.estado == "JUEGO":
    # Aquí aparecen los lances
    st.markdown("<p style='text-align:center; color:white;'>Apuestas actuales:</p>", unsafe_allow_html=True)
    l1, l2, l3, l4 = st.columns(4)
    l1.button("GRANDE", use_container_width=True)
    l2.button("CHICA", use_container_width=True)
    l3.button("PARES", use_container_width=True)
    l4.button("JUEGO", use_container_width=True)
    
    st.write("")
    if st.button("🔄 Nueva Mano / Limpiar Mesa", use_container_width=True):
        st.session_state.estado = "INICIO"
        st.rerun()
