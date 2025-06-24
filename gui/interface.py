# gui/interface.py

import tkinter as tk
from tkinter import simpledialog, messagebox
from core.drone import Drone
import random

TAMANHO_CELULA = 50
TAMANHO_MAPA = 10

class InterfaceDrone:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Missão de Drones")
        self.drone = Drone("DRN001", "Phantom Vision")
        self.mapa = [[0 for _ in range(TAMANHO_MAPA)] for _ in range(TAMANHO_MAPA)]
        self.x = 5
        self.y = 5

        self.canvas = tk.Canvas(root, width=TAMANHO_CELULA * TAMANHO_MAPA,
                                       height=TAMANHO_CELULA * TAMANHO_MAPA, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.legenda = tk.Canvas(root, width=220, height=180, bg="white")
        self.legenda.grid(row=0, column=4, rowspan=2, padx=10, pady=10, sticky="n")
        self.desenhar_legenda()

        self.botao_iniciar = tk.Button(root, text="Iniciar Missão", command=self.iniciar_missao)
        self.botao_iniciar.grid(row=1, column=0)

        self.botao_auto = tk.Button(root, text="Auto", command=self.simular_movimento_automatico)
        self.botao_auto.grid(row=1, column=1)

        self.botao_cima = tk.Button(root, text="↑", command=lambda: self.mover_drone(0, -1))
        self.botao_cima.grid(row=2, column=1)

        self.botao_baixo = tk.Button(root, text="↓", command=lambda: self.mover_drone(0, 1))
        self.botao_baixo.grid(row=4, column=1)

        self.botao_esquerda = tk.Button(root, text="←", command=lambda: self.mover_drone(-1, 0))
        self.botao_esquerda.grid(row=3, column=0)

        self.botao_direita = tk.Button(root, text="→", command=lambda: self.mover_drone(1, 0))
        self.botao_direita.grid(row=3, column=2)

        self.botao_finalizar = tk.Button(root, text="Finalizar Missão", command=self.finalizar_missao)
        self.botao_finalizar.grid(row=3, column=3)

        self.desenhar_mapa()

    def desenhar_legenda(self):
        categorias = [
            ("Ótima", "#00FF00"),
            ("Moderada", "#FFFF00"),
            ("Insalubre (sensíveis)", "#FFA500"),
            ("Insalubre", "#FF0000"),
            ("Muito insalubre", "#800080"),
            ("Perigosa", "#8B0000")
        ]
        self.legenda.delete("all")
        self.legenda.create_text(110, 10, text="Qualidade do Ar", font=("Arial", 10, "bold"))
        for i, (label, color) in enumerate(categorias):
            y = 30 + i * 25
            self.legenda.create_rectangle(10, y, 30, y + 20, fill=color, outline="black")
            self.legenda.create_text(120, y + 10, anchor="w", text=label, font=("Arial", 9))

    def desenhar_mapa(self):
        self.canvas.delete("all")
        for linha in range(TAMANHO_MAPA):
            for coluna in range(TAMANHO_MAPA):
                x0 = coluna * TAMANHO_CELULA
                y0 = linha * TAMANHO_CELULA
                x1 = x0 + TAMANHO_CELULA
                y1 = y0 + TAMANHO_CELULA

                cor = "lightgray"

                if self.drone.missao_ativa:
                    atual = self.drone.missao_ativa.pontos_voo.inicio
                    while atual:
                        ponto = atual.dado
                        if ponto.coordenadas == (coluna, linha):
                            _, cor = ponto.categoria_poluicao()
                            break
                        atual = atual.proximo

                if linha == self.y and coluna == self.x:
                    cor = "blue"  # Drone

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor, outline="black")

    def iniciar_missao(self):
        if self.drone.missao_ativa is not None:
            messagebox.showwarning("Aviso", "Já existe uma missão em andamento.")
            return

        tipo = simpledialog.askstring("Tipo de Missão", "Digite o tipo da missão:")
        if not tipo:
            return

        self.drone.iniciar_missao(tipo)
        self.x, self.y = 5, 5
        self.drone.registrar_ponto_voo(self.x, self.y)
        self.desenhar_mapa()

    def mover_drone(self, dx, dy):
        if self.drone.missao_ativa is None:
            messagebox.showwarning("Erro", "Inicie uma missão primeiro!")
            return

        novo_x = self.x + dx
        novo_y = self.y + dy

        if 0 <= novo_x < TAMANHO_MAPA and 0 <= novo_y < TAMANHO_MAPA:
            self.x = novo_x
            self.y = novo_y
            self.drone.registrar_ponto_voo(self.x, self.y)
            self.desenhar_mapa()
        else:
            messagebox.showwarning("Movimento inválido", "O drone não pode sair do mapa.")

    def simular_movimento_automatico(self):
        if self.drone.missao_ativa is None:
            messagebox.showwarning("Erro", "Inicie uma missão primeiro!")
            return

        passos = 10
        for _ in range(passos):
            direcao = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            novo_x = self.x + direcao[0]
            novo_y = self.y + direcao[1]

            if 0 <= novo_x < TAMANHO_MAPA and 0 <= novo_y < TAMANHO_MAPA:
                self.x = novo_x
                self.y = novo_y
                self.drone.registrar_ponto_voo(self.x, self.y)
                self.desenhar_mapa()
                self.root.update()
                self.root.after(250)

    def finalizar_missao(self):
        if self.drone.missao_ativa is None:
            messagebox.showinfo("Info", "Nenhuma missão ativa.")
            return

        self.drone.finalizar_missao()
        self.desenhar_mapa()
        self.exibir_relatorio()

    def exibir_relatorio(self):
        relatorios = []
        atual = self.drone.missoes.inicio
        while atual:
            relatorio = atual.dado.gerar_relatorio()
            texto = "\n".join(f"{k}: {v}" for k, v in relatorio.items())
            relatorios.append(texto)
            atual = atual.proximo

        if relatorios:
            messagebox.showinfo("Relatório de Missão", "\n\n---\n\n".join(relatorios))

def iniciar_interface():
    root = tk.Tk()
    app = InterfaceDrone(root)
    root.mainloop()