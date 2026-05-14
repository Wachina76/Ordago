import streamlit as st
import random
import os

# --- MOTOR DE INTELIGENCIA RIVAL (Conoce sus cartas y las reglas) ---
def evaluar_fuerza_ia(mano, lance):
    nums = [c['num'] for c in mano]
    # Grande: Reyes (12, 3). Chica: Ases (1, 2)
    if lance == "GRANDE": return sum(1 for n in nums if n in [12, 3])
    if lance == "CHICA": return sum(1 for n in nums if n in [1, 2])
    if lance == "PARES":
        counts = {n: nums.count(n) for n in set(nums)}
        # 31 es la mejor jugada (3 puntos), Medias valen 2
        if 4 in counts.values(): return 4 # Duples
        if 3 in counts.values(): return 3 # Medias
        if list(counts.values()).count(2) == 2: return 4 # Duples
        return 2 if 2 in counts.values() else 0
    return 0

# --- INICIALIZACIÓN ---
if 'estado' not in st.session_state:
    st.session_state.update({
        'estado': "INICIO", 
        'nombres': {'izq': "Rival 1", 'arriba': "Compañero", 'der': "Rival 2"},
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'lance_idx': 0,
        'historial': "Mesa lista. La IA ya sabe jugar con sus cartas.",
        'baraja': []
    })

# --- DISEÑO Y VISIBILIDAD ---
st.markdown("""
    <style>
    .stApp { background: #0e3311; color: white; }
    .marcador { background: #1a1a1a; color: #FFD700; padding: 10px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; font-weight: bold; }
    .consola { background: rgba(255,255,255,0.1); color: #00FF00; padding: 15px; border-radius: 10px; text-align: center; font-family: monospace; border: 1px solid #444; }
    .carta-slot { background: rgba(0,0,0,0.3); border-radius: 5px; padding: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA (Marcador) ---
c1, c2 = st.columns(2)
with c1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

# --- TABLERO COMPACTO ---
def mostrar_mesa(clave, titulo, visible=False):
    st.write(f"**{titulo}**")
    mano = st.session_state.partida.get(clave, [])
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("🗑️" if i in st.session_state.seleccionados else "OK", key=f"sel_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()
            
            img_path = os.path.join("img", f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png")
            if os.path.exists(img_path): st.image(img_path, width=70)
            else: st.markdown(f"<div class='carta-slot'>{c['num']}</div>", unsafe_allow_html=True)

# Distribución de la mesa
_, t_col, _ = st.columns([1,2,1])
with t_col: mostrar_mesa('arriba', "TU PAREJA", st.session_state.estado == "REVELAR")

l_col, m_col, r_col = st.columns([1,1.5,1])
with l_col: mostrar_mesa('izq', "RIVAL IZQ", st.session_state.estado == "REVELAR")
with m_col: st.markdown(f'<div class="consola">{st.session_state.historial}</div>', unsafe_allow_html=True)
with r_col: mostrar_mesa('der', "RIVAL DER", st.session_state.estado == "REVELAR")

_, b_col, _ = st.columns([1,2,1])
with b_col: mostrar_mesa('jugador', "TUS CARTAS (LUIS)", True)

# --- ACCIONES Y LÓGICA DE IA ---
st.divider()
if st.session_state.estado == "INICIO":
    if st.button("REPARTIR CARTAS", use_container_width=True, type="primary"):
        # Baraja reglamentaria
        palos = ['oros', 'copas', 'espadas', 'bastos']
        nums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]
        random.shuffle(baraja)
        st.session_state.partida = {
            'jugador': baraja[0:4], 'izq': baraja[4:8], 
            'arriba': baraja[8:12], 'der': baraja[12:16]
        }
        st.session_state.baraja = baraja[16:]
        st.session_state.estado = "MUS"
        st.rerun()

elif st.session_state.estado == "MUS":
    c1, c2 = st.columns(2)
    if c1.button("HAY MUS", use_container_width=True):
        st.session_state.estado = "DESCARTE"
        st.rerun()
    if c2.button("CORTO EL MUS", use_container_width=True):
        st.session_state.estado = "JUEGO"
        st.rerun()

elif st.session_state.estado == "JUEGO":
    lance = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"][st.session_state.lance_idx]
    fuerza_rival = evaluar_fuerza_ia(st.session_state.partida['izq'], lance)
    
    st.write(f"Estamos en: **{lance}**")
    b1, b2, b3 = st.columns(3)
    
    if b1.button("PASO"):
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()
        
    if b2.button("ENVIDO (2)"):
        # La IA sabe si aceptar basándose en su fuerza
        if fuerza_rival >= 2:
            st.session_state.puntos['nosotros'] += 2
            st.session_state.historial = "El rival tiene cartas y acepta el envite."
        else:
            st.session_state.puntos['nosotros'] += 1
            st.session_state.historial = "El rival no tiene nada y se retira."
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

    if b3.button("ÓRDAGO"):
        if fuerza_rival >= 3:
            st.session_state.historial = "¡ÓRDAGO QUERIDO! Se muestran las cartas."
            st.session_state.estado = "REVELAR"
        else:
            st.session_state.puntos['nosotros'] += 1
            st.session_state.lance_idx += 1
            st.rerun()

elif st.session_state.estado == "REVELAR":
    if st.button("NUEVA MANO", use_container_width=True):
        st.session_state.estado = "INICIO"; st.session_state.lance_idx = 0; st.rerun()
