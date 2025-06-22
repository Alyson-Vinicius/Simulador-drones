# core/missao.py

from core.lista_encadeada import ListaEncadeada
from core.ponto_voo import PontoDeVoo
import time
from datetime import datetime

class Missao:
    def __init__(self, tipo: str):
        self.tipo = tipo  # Ex: "entrega", "monitoramento ambiental", "vigilância"
        self.data_inicio = datetime.now()
        self.data_fim = None
        self.pontos_voo = ListaEncadeada()

        # Estatísticas acumuladas
        self.total_distancia = 0
        self.total_bateria = 0
        self.total_poluição = 0
        self.total_densidade = 0
        self.total_vegetacao = 0
        self.contador_pontos = 0

    def registrar_ponto(self, x, y):
        ponto = PontoDeVoo(x, y)
        self.pontos_voo.inserir_final(ponto)

        # Atualização das métricas
        self.total_bateria += ponto.bateria
        self.total_poluição += ponto.poluicao_ar
        self.total_densidade += ponto.densidade_populacional
        self.total_vegetacao += ponto.areas_verdes
        self.contador_pontos += 1

    def finalizar_missao(self):
        self.data_fim = datetime.now()

    def tempo_total(self):
        if self.data_fim:
            return (self.data_fim - self.data_inicio).total_seconds()
        else:
            return (datetime.now() - self.data_inicio).total_seconds()

    def gerar_relatorio(self):
        if self.contador_pontos == 0:
            return "Nenhum ponto registrado."

        return {
            "Tipo de missão": self.tipo,
            "Duração (s)": round(self.tempo_total(), 2),
            "Pontos coletados": self.contador_pontos,
            "Média poluição": round(self.total_poluição / self.contador_pontos, 2),
            "Média densidade populacional": round(self.total_densidade / self.contador_pontos, 2),
            "Área média com vegetação (%)": round(self.total_vegetacao / self.contador_pontos, 2),
            "Eficiência energética (bateria média por ponto)": round(self.total_bateria / self.contador_pontos, 2)
        }
