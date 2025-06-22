from gui.interface import iniciar_interface

if __name__ == "__main__":
    iniciar_interface()

# main.py

from core.drone import Drone

def mostrar_mapa(mapa, pos_x, pos_y):
    for y in range(len(mapa)):
        linha = ""
        for x in range(len(mapa[y])):
            if x == pos_x and y == pos_y:
                linha += "[D]"  # Drone
            else:
                linha += "[ ]"
        print(linha)
    print()

def simular_missao_terminal():
    drone = Drone("DRN001", "Phantom Vision")
    mapa = [[0 for _ in range(10)] for _ in range(10)]  # Mapa 10x10
    x, y = 5, 5  # Posição inicial do drone no centro

    tipo = input("Digite o tipo da missão (entrega / monitoramento / vigilância): ").strip()
    drone.iniciar_missao(tipo)

    print("\nControles: w = cima | s = baixo | a = esquerda | d = direita | f = finalizar missão")
    mostrar_mapa(mapa, x, y)
    drone.registrar_ponto_voo(x, y)

    while True:
        comando = input("Mover: ").strip().lower()

        if comando == "f":
            drone.finalizar_missao()
            break
        elif comando == "w" and y > 0:
            y -= 1
        elif comando == "s" and y < 9:
            y += 1
        elif comando == "a" and x > 0:
            x -= 1
        elif comando == "d" and x < 9:
            x += 1
        else:
            print("Movimento inválido.")
            continue

        drone.registrar_ponto_voo(x, y)
        mostrar_mapa(mapa, x, y)

    print("\n✅ Missão finalizada. Relatório:")
    drone.listar_missoes()


if __name__ == "__main__":
    simular_missao_terminal()
