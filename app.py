import streamlit as st
import random
import os

# --- MOTOR DE INTELIGENCIA (Luis, aquí es donde la IA "mira" sus cartas) ---
def evaluar_fuerza_ia(mano, lance):
    nums = [c['num'] for c in mano]
    if lance == "GRANDE": return sum(1 for n in nums if n in [12, 3])
    if lance == "CHICA": return sum(1 for n in nums if n in [1, 2])
    if lance == "PARES":
        counts = {n: nums.count(n) for n in set(nums)}
        if 4 in counts.values(): return 4 # Duples
        if 3 in counts.values(): return 3 # Medias
        return 2 if 2 in counts.values() else 0
    return 0

# --- INICIALIZACIÓN ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'nombres': {'izq': "Paco", 'arriba': "Tu Pareja", 'der': "Lola"},
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'lance_idx': 0,
        'historial': "¡Vamos Luis! IA agresiva y descarte arreglado.",
        'baraja': [],
        'descartadas': []
    })

# --- ESTILO VISUAL MEJORADO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b2e0b; color: white; }
    .marcador-caja { background: #111; border: 2px solid #gold; padding: 10px; border-radius: 10px; text-align: center; color: gold; font-size: 1.2rem; }
    .zona-descarte { background: #c65106; padding: 15px; border-radius: 10px; border: 2px solid white; margin: 10px 0; }
    .consola { background: black; color: #0f0; padding: 10px; border-radius: 5px; border: 1px solid #333; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
m1, m2 = st.columns(2)
m1.markdown(f'<div class="marcador-caja">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
m2.markdown(f'<div class="marcador-caja">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

def mostrar_mano(clave, titulo, visible=False):
    st.write(f"**{titulo}**")
    mano = st.session_state.partida.get(clave, [])
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            # INTERFAZ DE SELECCIÓN (Solo para Luis)
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("🗑️" if i in st.session_state.seleccionados else "✅", key=f"sel_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()
            
            img_path = os.path.join("img", f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png")
            if os.path.exists(img_path): st.image(img_path, width=75)
            else: st.button(f"{c['num']}-{c['palo'][0]}", disabled=True)

# --- MESA ---
st.write("---")
col_izq, col_cen, col_der = st.columns([1, 2, 1])
with col_izq: mostrar_mano('izq', "Rival Izq")
with col_cen:
    mostrar_mano('arriba', "Tu Pareja")
    st.markdown(f'<div class="consola">{st.session_state.historial}</div>', unsafe_allow_html=True)
with col_der: mostrar_mano('der', "Rival Der")

st.write("---")
mostrar_mano('jugador', "TU MANO (LUIS)", visible=True)

# --- PANEL DE BOTONES (Lógica de Descarte) ---
if st.session_state.estado == "INICIO":
    if st.button("🧧 EMPEZAR PARTIDA", use_container_width=True, type="primary"):
        palos = ['oros', 'copas', 'espadas', 'bastos']
        nums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
        random.shuffle(baraja)
        st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
        st.session_state.baraja = baraja[16:]
        st.session_state.estado = "MUS"
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("HAY MUS", use_container_width=True):
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if c2.button("CORTO (A JUGAR)", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "DESCARTE":
    st.markdown('<div class="zona-descarte">', unsafe_allow_html=True)
    st.write(f"Selecciona las cartas que NO quieres y pulsa el botón:")
    if st.button(f"🔥 DESCARTAR {len(st.session_state.seleccionados)} CARTAS Y PEDIR NUEVAS", use_container_width=True):
        # 1. Luis cambia cartas
        for i in st.session_state.seleccionados:
            st.session_state.partida['jugador'][i] = st.session_state.baraja.pop(0)
        # 2. La IA también se descarta (se queda Reyes/Ases)
        for k in ['izq', 'der', 'arriba']:
            st.session_state.partida[k] = [c if c['num'] in [12, 1, 3, 2] else st.session_state.baraja.pop(0) for c in st.session_state.partida[k]]
        
        st.session_state.seleccionados = []
        st.session_state.estado = "MUS"
        st.session_state.historial = "Cartas cambiadas. ¿Hay mus de nuevo?"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.estado == "JUEGO":
    lance = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"][st.session_state.lance_idx]
    fuerza_rival = evaluar_fuerza_ia(st.session_state.partida['izq'], lance)
    
    st.write(f"LANCE: **{lance}**")
    b1, b2, b3 = st.columns(3)
    if b1.button("PASO"):
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
    if b2.button("ENVIDO"):
        if fuerza_rival >= 2:
            st.session_state.puntos['nosotros'] += 2
            st.session_state.historial = "¡Te han querido el envite!"
        else:
            st.session_state.puntos['nosotros'] += 1
            st.session_state.historial = "Se achican. +1 piedra."
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
