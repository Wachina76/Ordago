def get_image_url(carta):
    # Base de imágenes de baraja española (Fournier)
    # Formato: https://raw.githubusercontent.com/profe-js/baraja-espanola/main/img/palo_numero.png
    
    palo_map = {
        'Oros': 'oros', 
        'Copas': 'copas', 
        'Espadas': 'espadas', 
        'Bastos': 'bastos'
    }
    
    # Mapeo de caras a números reales de la baraja
    cara_map = {
        'R': 12, 'C': 11, 'S': 10, 
        '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'A': 1
    }
    
    palo = palo_map[carta['palo']]
    num = cara_map[carta['cara']]
    
    # Esta es una URL de un repositorio público muy estable
    return f"https://raw.githubusercontent.com/poker-fichas/cartas/main/spanish/{palo}_{num}.png"
