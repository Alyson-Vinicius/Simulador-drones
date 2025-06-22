# testes/teste_listas.py

from core.lista_encadeada import ListaEncadeada
from core.ponto_voo import PontoDeVoo

lista = ListaEncadeada()

for i in range(5):
    ponto = PontoDeVoo(x=i, y=i+1)
    lista.inserir_final(ponto)

print("Lista de Pontos de Voo:")
print(lista.exibir())


# testes/teste_missao.py

from core.missao import Missao
import time

missao = Missao("monitoramento ambiental")

for i in range(5):
    missao.registrar_ponto(x=i, y=i+1)
    time.sleep(0.5)  # Simula tempo real

missao.finalizar_missao()
relatorio = missao.gerar_relatorio()

print("Relatório da Missão:")
for chave, valor in relatorio.items():
    print(f"{chave}: {valor}")


# testes/teste_drone.py

from core.drone import Drone
import time

drone = Drone("DRN001", "Phantom Vision")

drone.iniciar_missao("entrega")
for i in range(3):
    drone.registrar_ponto_voo(i, i + 1)
    time.sleep(0.5)

drone.finalizar_missao()

drone.iniciar_missao("vigilância")
for i in range(2):
    drone.registrar_ponto_voo(i + 3, i + 4)
    time.sleep(0.5)

drone.finalizar_missao()

print("\n=== Histórico de Missões ===")
drone.listar_missoes()
