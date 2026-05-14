import streamlit as st
import random
import os

# --- MOTOR DEL JUEGO ---
def crear_baraja_mus():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [{'num': n, 'palo': p} for p in palos for n in numeros]

if 'mano' not in st.session_state:
    st.session_state.mano = []

# --- INTERFAZ ---
st.title("🃏 Órdago Mus")

if st.button("REPARTIR"):
    baraja = crear_baraja_mus()
    random.shuffle(baraja)
    st.session_state.mano = baraja[:4]
    st.rerun()

# --- MOSTRAR CARTAS ---
if st.session_state.mano:
    cols = st.columns(4)
    for i, carta in enumerate(st.session_state.mano):
        with cols[i]:
            # IMPORTANTE: El nombre debe coincidir con tus archivos en GitHub
            # Si tus archivos son "Oros_1.png", aquí debe ser igual.
            nombre_archivo = f"{carta['palo']}_{carta['num']}.png"
            
            # Buscamos la imagen en la carpeta 'img' que está en la raíz
            ruta_imagen = os.path.join("img", nombre_archivo)
            
            if os.path.exists(ruta_imagen):
                st.image(ruta_imagen, use_container_width=True)
            else:
                st.error(f"No encontrada")
                st.caption(nombre_archivo) # Esto te dirá qué nombre está fallando
