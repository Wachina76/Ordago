import streamlit as st
from engine import crear_baraja, repartir

st.set_page_config(page_title="Mus Real", layout="centered")

# Diccionario para convertir nombres de cartas a URLs de imágenes
# Nota: Usamos una base de imágenes de Wikimedia o similar
BASE_URL = "https://raw.githubusercontent.com/saulmaldonado/spanish-deck/master/cards/"

def get_image_url(carta):
    palo_map = {'Oros': 'oros', 'Copas': 'copas', 'Espadas': 'espadas', 'Bastos': 'bastos'}
    # Mapeo de caras a números de imagen (R=12, C=11, S=10, etc.)
    cara_map = {'R': 12, 'C': 11, 'S': 10, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'A': 1}
    
    palo = palo_map[carta['palo']]
    num = cara_map[carta['cara']]
    return f"{BASE_URL}{palo}_{num}.png"

# --- LÓGICA DE ESTADO ---
if 'mano' not in st.session_state:
    st.session_state.mano = []

st.title("🃏 Mus Profesional")

if st.button("🎴 Repartir Cartas"):
    baraja = crear_baraja()
    st.session_state.mano = repartir(baraja)[0]

# --- RENDERIZADO DE CARTAS ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            url = get_image_url(carta)
            # Mostramos la imagen de la carta
            st.image(url, use_container_width=True)
            st.caption(f"{carta['cara']} de {carta['palo']}")

# --- BOTONES DE JUEGO ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("👍 Paso"): st.info("Pasas")
with c2:
    if st.button("💰 Envido"): st.warning("¡Envido!")
with c3:
    if st.button("🔥 Órdago"): st.error("¡ÓRDAGO!")
with c4:
    if st.button("🤫 Seña"): st.toast("Has hecho una seña a tu socio")

