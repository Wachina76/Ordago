import random
from engine import analizar_pares, analizar_juego

class IA:
    def __init__(self, nombre, personalidad="equilibrada"):
        self.nombre = nombre
        self.personalidad = personalidad

    def decidir_accion(self, mano, lance, apuesta_actual):
        fuerza = random.randint(1, 10) # Simulación simplificada de decisión
        if apuesta_actual == 0:
            return "envido" if fuerza > 7 else "paso"
        else:
            return "quiero" if fuerza > 4 else "paso"

    def emitir_sena(self, mano):
        p = analizar_pares(mano)
        if p and p['tipo'] == "duples": return "LEVANTAR CEJAS"
        return None