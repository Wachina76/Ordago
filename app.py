import streamlit as st
import os

def mostrar_carta(palo, num):
    # Intentamos encontrar la carpeta 'img'
    # 1. Probar en la raíz
    ruta_raiz = os.path.join("img", f"{palo}_{num}.png")
    # 2. Probar dentro de la carpeta 'mus' (por si acaso)
    ruta_mus = os.path.join("mus", "img", f"{palo}_{num}.png")
    
    if os.path.exists(ruta_raiz):
        st.image(ruta_raiz, use_container_width=True)
    elif os.path.exists(ruta_mus):
        st.image(ruta_mus, use_container_width=True)
    else:
        st.error(f"No encuentro: {palo}_{num}.png")
        st.write(f"Buscado en: {ruta_raiz} y {ruta_mus}")
