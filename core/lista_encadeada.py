# core/lista_encadeada.py

class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.inicio = None

    def esta_vazia(self):
        return self.inicio is None

    def inserir_final(self, dado):
        novo_no = No(dado)
        if self.esta_vazia():
            self.inicio = novo_no
        else:
            atual = self.inicio
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no

    def remover(self, dado):
        if self.esta_vazia():
            return False
        atual = self.inicio
        anterior = None
        while atual:
            if atual.dado == dado:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def buscar(self, dado):
        atual = self.inicio
        while atual:
            if atual.dado == dado:
                return atual
            atual = atual.proximo
        return None

    def tamanho(self):
        contador = 0
        atual = self.inicio
        while atual:
            contador += 1
            atual = atual.proximo
        return contador

    def exibir(self):
        elementos = []
        atual = self.inicio
        while atual:
            elementos.append(str(atual.dado))
            atual = atual.proximo
        return " -> ".join(elementos)
