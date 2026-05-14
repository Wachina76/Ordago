import streamlit as st
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mus Fournier - IA Agresiva", layout="wide")

# --- MOTOR DE INTELIGENCIA RIVAL ---
def ia_decide_jugar(mano, lance, envite_jugador=0):
    """
    La IA analiza su fuerza y decide si PASA, VE, ENVIDA o lanza ÓRDAGO.
    """
    nums = [c['num'] for c in mano]
    # Fuerza basada en Reyes (12, 3) para Grande o Ases (1, 2) para Chica
    fuerza = sum(1 for n in nums if n in ([12, 3] if lance == "GRANDE" else [1, 2]))
    
    # Lógica de decisión
    if envite_jugador > 0:
        if fuerza >= 3: return "ÓRDAGO"
        if fuerza >= 1: return "QUIERO"
        return "FUERA"
    
    if fuerza >= 2: return "ENVIDO"
    return "PASO"

# --- INICIALIZACIÓN ---
if 'estado' not in st.session_state:
    rivales = random.sample(["Paco", "Lola", "Curro", "Elena", "Pepe", "Marta"], 3)
    st.session_state.update({
        'estado': "INICIO", 
        'nombres': {'izq': rivales[0], 'arriba': rivales[1], 'der': rivales[2]},
        'partida': {'jugador': [], 'izq': [], 'der': [], 'arriba': []},
        'puntos': {'nosotros': 0, 'ellos': 0},
        'seleccionados': [],
        'lance_idx': 0,
        'historial': "IA actualizada: Ahora son agresivos y van al Órdago.",
        'es_mano': 'jugador'
    })

LANCES = ["GRANDE", "CHICA", "PARES", "JUEGO/PUNTO"]

# --- CSS Y ESTILO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a4a1a 0%, #0d260d 100%); }
    .consola-central { background: rgba(0,0,0,0.95); color: #0f0; font-family: monospace; padding: 15px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; }
    .marcador { background: #222; color: gold; padding: 10px; border-radius: 10px; text-align: center; font-size: 1.5rem; font-weight: bold; border: 2px solid #444;}
    .label-jugador { color: #FFD700; text-align: center; background: rgba(0,0,0,0.7); padding: 5px; border-radius: 5px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- INTERFAZ ---
m1, m2 = st.columns(2)
with m1: st.markdown(f'<div class="marcador">NOSOTROS: {st.session_state.puntos["nosotros"]}</div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="marcador">ELLOS: {st.session_state.puntos["ellos"]}</div>', unsafe_allow_html=True)

def dibujar_mano(clave, titulo, visible=False):
    st.markdown(f'<div class="label-jugador">{titulo}</div>', unsafe_allow_html=True)
    mano = st.session_state.partida[clave]
    if not mano: return
    cols = st.columns(4)
    for i, c in enumerate(mano):
        with cols[i]:
            # Botones de descarte visibles arriba de la carta
            if clave == 'jugador' and st.session_state.estado == "DESCARTE":
                if st.button("🗑️" if i in st.session_state.seleccionados else "✅", key=f"d_{i}"):
                    if i in st.session_state.seleccionados: st.session_state.seleccionados.remove(i)
                    else: st.session_state.seleccionados.append(i)
                    st.rerun()
            img = os.path.join("img", f"{str(c['num']).zfill(2)}-{c['palo']}.png" if visible else "reverso.png")
            if os.path.exists(img): st.image(img)

# Mesa
st.columns([1, 1, 1])[1].write(dibujar_mano('arriba', st.session_state.nombres['arriba'], st.session_state.estado == "REVELAR"))
c_izq, c_mid, c_der = st.columns([1, 1.5, 1])
with c_izq: dibujar_mano('izq', st.session_state.nombres['izq'], st.session_state.estado == "REVELAR")
with c_mid:
    st.markdown(f'<div class="consola-central"><b>{LANCES[st.session_state.lance_idx] if st.session_state.estado == "JUEGO" else st.session_state.estado}</b><br>{st.session_state.historial}</div>', unsafe_allow_html=True)
with c_der: dibujar_mano('der', st.session_state.nombres['der'], st.session_state.estado == "REVELAR")
st.columns([1, 1, 1])[1].write(dibujar_mano('jugador', "YO", True))

# --- LÓGICA DE BOTONES ---
st.write("---")
if st.session_state.estado == "INICIO":
    if st.button("🧧 REPARTIR", use_container_width=True):
        palos, nums = ['oros', 'copas', 'espadas', 'bastos'], [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        baraja = [{'num': n, 'palo': p} for p in palos for n in nums]; random.shuffle(baraja)
        st.session_state.partida = {'jugador': baraja[0:4], 'izq': baraja[4:8], 'arriba': baraja[8:12], 'der': baraja[12:16]}
        st.session_state.estado = "MUS"; st.rerun()

elif st.session_state.estado == "MUS":
    col1, col2 = st.columns(2)
    if col1.button("✅ PEDIR MUS", use_container_width=True): st.session_state.estado = "DESCARTE"; st.rerun()
    if col2.button("❌ CORTAR", use_container_width=True): st.session_state.estado = "JUEGO"; st.rerun()

elif st.session_state.estado == "DESCARTE":
    if st.button(f"♻️ CAMBIAR SELECCIONADAS ({len(st.session_state.seleccionados)})", use_container_width=True):
        st.session_state.estado = "MUS"; st.session_state.seleccionados = []; st.rerun()

elif st.session_state.estado == "JUEGO":
    lance = LANCES[st.session_state.lance_idx]
    b1, b2, b3 = st.columns(3)
    
    if b1.button("PASO", use_container_width=True):
        dec = ia_decide_jugar(st.session_state.partida['izq'], lance)
        if dec == "ENVIDO":
            st.session_state.historial = f"{st.session_state.nombres['izq']} te ENVIDA a ti."; st.session_state.puntos['ellos'] += 1
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

    if b2.button("ENVIDO (2)", use_container_width=True):
        dec = ia_decide_jugar(st.session_state.partida['izq'], lance, envite_jugador=2)
        if dec == "QUIERO":
            st.session_state.historial = "¡Te han QUERIDO el envite!"; st.session_state.puntos['nosotros'] += 2
        elif dec == "ÓRDAGO":
            st.session_state.historial = "¡TE RESPONDEN CON ÓRDAGO!"; st.session_state.puntos['ellos'] += 2
        else:
            st.session_state.historial = "Se achican. +1 piedra."; st.session_state.puntos['nosotros'] += 1
        st.session_state.lance_idx += 1
        if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

    if b3.button("ÓRDAGO", use_container_width=True):
        dec = ia_decide_jugar(st.session_state.partida['izq'], lance, envite_jugador=40)
        if dec == "QUIERO" or dec == "ÓRDAGO":
            st.session_state.historial = "¡HAN QUERIDO EL ÓRDAGO!"; st.session_state.estado = "REVELAR"
        else:
            st.session_state.historial = "No quieren. +1 punto."; st.session_state.puntos['nosotros'] += 1
            st.session_state.lance_idx += 1
            if st.session_state.lance_idx >= 4: st.session_state.estado = "REVELAR"
        st.rerun()

elif st.session_state.estado == "REVELAR":
    if st.button("🔄 SIGUIENTE MANO", use_container_width=True):
        st.session_state.estado = "INICIO"; st.session_state.lance_idx = 0; st.rerun()
