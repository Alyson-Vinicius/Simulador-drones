# core/drone.py

from core.lista_encadeada import ListaEncadeada
from core.missao import Missao

class Drone:
    def __init__(self, identificador: str, modelo: str):
        self.identificador = identificador  # Ex: DRN001
        self.modelo = modelo                # Ex: DJI Phantom X
        self.missoes = ListaEncadeada()
        self.missao_ativa = None

    def iniciar_missao(self, tipo_missao: str):
        if self.missao_ativa is not None:
            print("Já existe uma missão em andamento. Finalize antes de iniciar outra.")
            return

        nova = Missao(tipo_missao)
        self.missao_ativa = nova
        print(f"Missão '{tipo_missao}' iniciada.")

    def registrar_ponto_voo(self, x, y):
        if self.missao_ativa is None:
            print("Nenhuma missão ativa para registrar ponto.")
            return

        self.missao_ativa.registrar_ponto(x, y)

    def finalizar_missao(self):
        if self.missao_ativa is None:
            print("Nenhuma missão ativa para finalizar.")
            return

        self.missao_ativa.finalizar_missao()
        self.missoes.inserir_final(self.missao_ativa)
        print(f"Missão '{self.missao_ativa.tipo}' finalizada.")
        self.missao_ativa = None

    def listar_missoes(self):
        atual = self.missoes.inicio
        contador = 1
        while atual:
            relatorio = atual.dado.gerar_relatorio()
            print(f"\n📋 Missão {contador}")
            for chave, valor in relatorio.items():
                print(f"{chave}: {valor}")
            atual = atual.proximo
            contador += 1

    def __str__(self):
        return f"Drone {self.identificador} - Modelo: {self.modelo}"
