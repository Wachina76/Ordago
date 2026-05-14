import streamlit as st
import time
from engine import crear_baraja, repartir, comparar_manos

# Configuración de la página
st.set_page_config(page_title="Mus Online", page_icon="🃏")

# Estilo para las cartas con colores
def estilo_carta(carta):
    color = "red" if carta['palo'] in ['Copas', 'Oros'] else "black"
    return f"""
    <div style="border: 2px solid gray; border-radius: 10px; padding: 10px; 
                width: 60px; height: 90px; text-align: center; display: inline-block; 
                margin: 5px; background-color: white; color: {color}; font-weight: bold;">
        {carta['cara']}<br>{carta['palo'][0]}
    </div>
    """

# Inicializar el estado del juego si no existe
if 'marcador' not in st.session_state:
    st.session_state.marcador = {"Pareja A": 0, "Pareja B": 0}
    st.session_state.mano_jugador = []
    st.session_state.partida_iniciada = False

st.title("🃏 Gran Mus Web")

# Marcador visual
col1, col2 = st.columns(2)
col1.metric("Tu Equipo", st.session_state.marcador["Pareja A"])
col2.metric("Rivales", st.session_state.marcador["Pareja B"])

if st.button("Repartir Nueva Mano"):
    baraja = crear_baraja()
    manos = repartir(baraja)
    st.session_state.mano_jugador = manos[0]
    st.session_state.partida_iniciada = True

if st.session_state.partida_iniciada:
    st.subheader("Tus Cartas:")
    # Mostrar cartas con colores
    cartas_html = "".join([estilo_carta(c) for c in st.session_state.mano_jugador])
    st.markdown(cartas_html, unsafe_allow_html=True)

    st.subheader("¿Qué quieres hacer?")
    c1, c2, c3 = st.columns(3)
    
    if c1.button("PASO"):
        st.info("Has pasado. Esperando a la IA...")
        # Aquí llamarías a la lógica de ia.py
        
    if c2.button("ENVIDO"):
        st.warning("¡Has envidado 2 tantos!")
        
    if c3.button("ÓRDAGO"):
        st.error("¡ÓRDAGO A LA GRANDE!")