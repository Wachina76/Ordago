import streamlit as st
import random
import os

# --- MOTOR DE INTELIGENCIA RIVAL (Sabe lo que tiene) ---
def evaluar_fuerza_real(mano, lance):
    nums = [c['num'] for c in mano]
    # Grande: Reyes (12, 3). Chica: Ases (1, 2)
    if lance == "GRANDE": return sum(1 for n in nums if n in [12, 3])
    if lance == "CHICA": return sum(1 for n in nums if n in [1, 2])
    if lance == "PARES":
        counts = {n: nums.count(n) for n in set(nums)}
        return max(counts.values()) if counts else 0
    if lance == "JUEGO/PUNTO":
        suma = sum([min(c['num'], 10) for c in mano])
        return 3 if suma == 31 else (2 if suma > 30 else 1)
    return 0

# --- INICIALIZACIÓN ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'nombres': {'izq': "Paco", 'arriba': "Compañero", 'der': "Lola"},
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'lance_idx': 0,
        'historial': "IA con conocimiento de normas activada.",
        'baraja': []
    })

# --- INTERFAZ COMPACTA ---
st.markdown("<style>.stApp { background: #1a4a1a; color: gold; }</style>", unsafe_allow_html=True)

# Lógica de descarte mejorada
if st.session_state.estado == "DESCARTE":
    if st.button(f"CONFIRMAR CAMBIO ({len(st.session_state.seleccionados)} cartas)", use_container_width=True):
        # El jugador cambia sus seleccionadas
        for i in st.session_state.seleccionados:
            st.session_state.partida['jugador'][i] = random.choice([{'num': n, 'palo': p} for p in ['oros','copas'] for n in [1,2,10,12]])
        # La IA solo cambia lo que no son Reyes/Ases
        for k in ['izq', 'der', 'arriba']:
            st.session_state.partida[k] = [c if c['num'] in [12, 1, 3, 2] else random.choice([{'num': n, 'palo': p} for p in ['oros','copas'] for n in [1,2,10,12]]) for c in st.session_state.partida[k]]
        st.session_state.estado = "MUS"
        st.session_state.seleccionados = []
        st.rerun()

# Botones de juego con IA que responde según su mano
if st.session_state.estado == "JUEGO":
    lance_actual = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"][st.session_state.lance_idx]
    fuerza_ia = evaluar_fuerza_real(st.session_state.partida['izq'], lance_actual)
    
    col1, col2 = st.columns(2)
    if col1.button("ENVIDO"):
        if fuerza_ia >= 2: # La IA sabe que tiene buena mano y acepta
            st.session_state.puntos['nosotros'] += 2
            st.session_state.historial = f"La IA ve tus cartas, sabe que tiene algo y QUIERE."
        else:
            st.session_state.puntos['nosotros'] += 1
            st.session_state.historial = "La IA reconoce que su mano es débil y se retira."
        st.session_state.lance_idx += 1
        st.rerun()
