import random

# Jerarquía oficial del Mus: R, 3, C, S, 7, 6, 5, 4, 2, A
JERARQUIA = ['R', '3', 'C', 'S', '7', '6', '5', '4', '2', 'A']

# Valores para sumar puntos en Juego (31, 40, etc.)
VALORES_SUMA = {
    'R': 10, '3': 10, 'C': 10, 'S': 10,
    '7': 7, '6': 6, '5': 5, '4': 4,
    '2': 1, 'A': 1
}

def crear_baraja():
    palos = ['Oros', 'Copas', 'Espadas', 'Bastos']
    caras = ['R', '3', 'C', 'S', '7', '6', '5', '4', '2', 'A']
    return [{'cara': c, 'palo': p} for c in caras for p in palos]

def repartir(baraja):
    random.shuffle(baraja)
    return [baraja[i:i + 4] for i in range(0, 16, 4)]

def analizar_pares(mano):
    caras = [c['cara'] for c in mano]
    conteos = {c: caras.count(c) for c in set(caras)}
    frecuencias = sorted(conteos.values(), reverse=True)
    cartas_con_par = sorted([c for c, count in conteos.items() if count >= 2], 
                            key=lambda x: JERARQUIA.index(x))

    if 4 in frecuencias or frecuencias == [2, 2]:
        return {"tipo": "duples", "fuerza": 3, "piedras": 3, "cartas": cartas_con_par}
    if 3 in frecuencias:
        return {"tipo": "medias", "fuerza": 2, "piedras": 2, "cartas": cartas_con_par}
    if 2 in frecuencias:
        return {"tipo": "par", "fuerza": 1, "piedras": 1, "cartas": cartas_con_par}
    return None

def analizar_juego(mano):
    suma = sum(VALORES_SUMA[c['cara']] for c in mano)
    ranking_juego = [31, 40, 37, 36, 35, 34, 33, 32]
    if suma >= 31:
        fuerza = 100 - (ranking_juego.index(suma) if suma in ranking_juego else 20)
        return {"tipo": "juego", "fuerza": fuerza, "piedras": (3 if suma == 31 else 2)}
    return {"tipo": "punto", "fuerza": suma, "piedras": 1}

def comparar_manos(mano1, mano2, lance):
    if lance == "grande":
        v1 = sorted([JERARQUIA.index(c['cara']) for c in mano1])
        v2 = sorted([JERARQUIA.index(c['cara']) for c in mano2])
        return 1 if v1 < v2 else 2
    elif lance == "chica":
        v1 = sorted([JERARQUIA.index(c['cara']) for c in mano1], reverse=True)
        v2 = sorted([JERARQUIA.index(c['cara']) for c in mano2], reverse=True)
        return 1 if v1 > v2 else 2
    elif lance == "pares":
        p1, p2 = analizar_pares(mano1), analizar_pares(mano2)
        if not p1: return 2
        if not p2: return 1
        if p1['fuerza'] != p2['fuerza']: return 1 if p1['fuerza'] > p2['fuerza'] else 2
        return 1 if JERARQUIA.index(p1['cartas'][0]) < JERARQUIA.index(p2['cartas'][0]) else 2
    elif lance == "juego":
        j1, j2 = analizar_juego(mano1), analizar_juego(mano2)
        return 1 if j1['fuerza'] > j2['fuerza'] else 2
    return 0