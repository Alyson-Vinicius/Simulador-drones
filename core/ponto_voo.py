import random

class PontoDeVoo:
    def __init__(self, x, y):
        self.coordenadas = (x, y)
        self.altitude = random.randint(10, 100)  # metros
        self.velocidade = random.uniform(10, 50)  # km/h
        self.direcao_vento = random.choice(["N", "S", "L", "O"])
        self.bateria = random.uniform(0, 100)  # %
        self.temperatura = random.uniform(15, 40)  # Celsius
        self.status_carga = random.choice(["com pacote", "sem pacote"])
        self.camera_ligada = random.choice([True, False])
        self.fotos = random.randint(0, 5)

        self.tipo_area = random.choice(["urbana", "residencial", "industrial", "rural", "mata", "zona de risco"])
        self.densidade_populacional = random.randint(0, 20000)  # hab/km²
        self.areas_verdes = random.uniform(0, 100)  # %
        self.poluicao_ar = random.uniform(0, 500)  # índice
        self.construcoes_altas = random.choice([True, False])
        self.sinal_gps = random.choice(["forte", "fraco", "perdido"])
        self.ruido = random.randint(30, 120)  # dB

    def __str__(self):
        return f"Ponto({self.coordenadas}, {self.tipo_area}, Poluição: {self.poluicao_ar:.2f})"

    def categoria_poluicao(self):
        p = self.poluicao_ar
        if p <= 50:
            return "Ótima", "#00FF00"
        elif p <= 100:
            return "Moderada", "#FFFF00"
        elif p <= 150:
            return "Insalubre (sensíveis)", "#FFA500"
        elif p <= 200:
            return "Insalubre", "#FF0000"
        elif p <= 300:
            return "Muito insalubre", "#800080"
        else:
            return "Perigosa", "#8B0000"