# gui/interface.py

import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import random
import time # Para simulação automática com pausa
import math # Para cálculo de distância

# =========================================================================
# CLASSES DE SUPORTE (TEMPORÁRIAS/ADAPTADAS)
# ATENÇÃO: ESTAS CLASSES DEVEM SER SUBSTITUÍDAS PELAS SUAS VERSÕES EM 'core/'
# ELAS ESTÃO AQUI APENAS PARA TORNAR ESTE ARQUIVO EXECUTÁVEL DE FORMA AUTÔNOMA
# E DEMONSTRAR AS FUNCIONALIDADES DA INTERFACE.
# =========================================================================

class No:
    """Representa um nó de uma lista encadeada."""
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeada:
    """Implementa uma lista encadeada simples."""
    def __init__(self):
        self.inicio = None
        self.fim = None # Adicionado para inserir_final mais eficiente

    def esta_vazia(self) -> bool:
        """Verifica se a lista está vazia."""
        return self.inicio is None

    def inserir_final(self, dado):
        """Insere um novo nó no final da lista."""
        novo_no = No(dado)
        if self.esta_vazia():
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

    def remover(self, dado) -> bool:
        """Remove o primeiro nó com o dado especificado."""
        if self.esta_vazia():
            return False
        atual = self.inicio
        anterior = None
        while atual:
            if atual.dado == dado:
                if anterior is None:
                    self.inicio = atual.proximo
                    if self.inicio is None: # Se a lista ficou vazia
                        self.fim = None
                else:
                    anterior.proximo = atual.proximo
                    if atual.proximo is None: # Se removeu o último
                        self.fim = anterior
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def buscar(self, dado):
        """Busca e retorna o nó com o dado especificado, ou None."""
        atual = self.inicio
        while atual:
            if atual.dado == dado:
                return atual
            atual = atual.proximo
        return None

    def tamanho(self) -> int:
        """Retorna o número de elementos na lista."""
        contador = 0
        atual = self.inicio
        while atual:
            contador += 1
            atual = atual.proximo
        return contador

    def to_list(self):
        """Converte a lista encadeada em uma lista Python."""
        items = []
        current = self.inicio
        while current:
            items.append(current.dado)
            current = current.proximo
        return items

    def __str__(self):
        return f"Lista com {self.tamanho()} elementos"


class PontoVoo:
    """
    Representa os dados coletados pelo drone em uma célula específica do mapa.
    Inclui dados de telemetria do drone e dados ambientais do local.
    """
    def __init__(self, x, y,
                 altitude=0, velocidade=0, direcao_vento="N", nivel_bateria=100,
                 temperatura_ambiente=25, status_carga="sem pacote", status_camera="desligada",
                 num_fotos_registradas=0,
                 tipo_area="urbana", densidade_populacional=0, presenca_areas_verdes=0,
                 indice_poluicao_ar=0, presenca_construcoes_altas="não",
                 sinal_gps="forte", intensidade_ruido=50):
        
        self.coordenadas = (x, y)
        # Dados de Telemetria (já usados com valores aleatórios no simulador)
        self.altitude = altitude
        self.velocidade = velocidade
        self.direcao_vento = direcao_vento
        self.nivel_bateria = nivel_bateria # Este será atualizado pelo drone
        self.temperatura_ambiente = temperatura_ambiente
        self.status_carga = status_carga
        self.status_camera = status_camera
        self.num_fotos_registradas = num_fotos_registradas
        
        # Dados do Ambiente Sobrevoado (gerados aleatoriamente ou mapeados)
        self.tipo_area = tipo_area
        self.densidade_populacional = densidade_populacional
        self.presenca_areas_verdes = presenca_areas_verdes
        self.indice_poluicao_ar = indice_poluicao_ar
        self.presenca_construcoes_altas = presenca_construcoes_altas
        self.sinal_gps = sinal_gps
        self.intensidade_ruido = intensidade_ruido

    def gerar_telemetria_aleatoria(self, current_battery):
        """Gera dados de telemetria aleatórios para este ponto de voo."""
        self.altitude = random.randint(30, 150)
        self.velocidade = random.randint(5, 30)
        self.direcao_vento = random.choice(["N", "NE", "E", "SE", "S", "SO", "O", "NO"])
        self.nivel_bateria = max(0, current_battery) # A bateria é passada e usada
        self.temperatura_ambiente = random.randint(15, 35)
        self.status_carga = random.choice(["com pacote", "sem pacote"])
        self.status_camera = random.choice(["ligada", "desligada"])
        self.num_fotos_registradas = random.randint(0, 5)

    def categoria_poluicao(self):
        """Retorna a categoria e a cor da poluição do ar com base no índice."""
        if self.indice_poluicao_ar <= 40:
            return "Ótima", "#00FF00" # Verde
        elif 41 <= self.indice_poluicao_ar <= 80:
            return "Moderada", "#FFFF00" # Amarelo
        elif 81 <= self.indice_poluicao_ar <= 120:
            return "Insalubre (sensíveis)", "#FFA500" # Laranja
        elif 121 <= self.indice_poluicao_ar <= 200:
            return "Insalubre", "#FF0000" # Vermelho
        elif 201 <= self.indice_poluicao_ar <= 300:
            return "Muito insalubre", "#800080" # Roxo
        else:
            return "Perigosa", "#8B0000" # Vermelho Escuro

    def to_dict(self):
        """Converte os dados do ponto de voo em um dicionário para exibição."""
        return {
            "Coordenadas": f"({self.coordenadas[0]}, {self.coordenadas[1]})",
            "Altitude": f"{self.altitude}m",
            "Velocidade": f"{self.velocidade} km/h",
            "Direção do Vento": self.direcao_vento,
            "Nível da Bateria": f"{self.nivel_bateria}%",
            "Temperatura Ambiente": f"{self.temperatura_ambiente}°C",
            "Status da Carga": self.status_carga,
            "Status da Câmera": self.status_camera,
            "Fotos Registradas": self.num_fotos_registradas,
            "Tipo de Área": self.tipo_area,
            "Densidade Populacional": f"{self.densidade_populacional} hab/km²",
            "Áreas Verdes": f"{self.presenca_areas_verdes}%",
            "Poluição do Ar (AQI)": f"{self.indice_poluicao_ar} ({self.categoria_poluicao()[0]})",
            "Construções Altas": self.presenca_construcoes_altas,
            "Sinal de GPS": self.sinal_gps,
            "Intensidade de Ruído": f"{self.intensidade_ruido} dB"
        }

    def __str__(self):
        return f"Ponto({self.coordenadas[0]},{self.coordenadas[1]}) - Bateria: {self.nivel_bateria}% - Poluição: {self.categoria_poluicao()[0]}"


class Missao:
    """
    Representa uma missão do drone, contendo seu tipo e um histórico de pontos de voo.
    Calcula estatísticas da missão após a finalização.
    """
    def __init__(self, tipo_missao: str):
        self.tipo = tipo_missao
        self.pontos_voo = ListaEncadeada() # Histórico de PontoVoo na missão
        self.tempo_inicio = time.time()
        self.tempo_fim = None
        self.distancia_total = 0.0
        self.bateria_consumida = 0
        self.densidade_pop_total = 0
        self.areas_verdes_total = 0
        self.poluicao_total = 0
        self.pontos_contados = 0

    def registrar_ponto(self, x, y, drone_battery, environmental_data):
        """Registra um PontoVoo na missão e atualiza estatísticas parciais."""
        ponto = PontoVoo(x, y, nivel_bateria=drone_battery, **environmental_data)
        # Gera telemetria aleatória, a bateria é passada e usada
        ponto.gerar_telemetria_aleatoria(drone_battery) 

        # Calcula a distância do último ponto (se houver)
        if not self.pontos_voo.esta_vazia():
            ultimo_ponto = self.pontos_voo.fim.dado # Acessa o dado do último nó
            distancia_segmento = math.sqrt((x - ultimo_ponto.coordenadas[0])**2 + (y - ultimo_ponto.coordenadas[1])**2)
            self.distancia_total += distancia_segmento # Assumindo 1 unidade = 1km ou 1 metro de célula

            # Calcula consumo de bateria para este segmento
            # Assumindo consumo de 1% por unidade de distância
            bateria_consumida_segmento = random.uniform(0.5, 1.5) * distancia_segmento
            self.bateria_consumida += bateria_consumida_segmento
            
        self.pontos_voo.inserir_final(ponto)

        # Acumula dados para estatísticas médias
        self.densidade_pop_total += ponto.densidade_populacional
        self.areas_verdes_total += ponto.presenca_areas_verdes
        self.poluicao_total += ponto.indice_poluicao_ar
        self.pontos_contados += 1


    def finalizar_missao(self):
        """Finaliza a missão e calcula as estatísticas finais."""
        if self.tempo_fim is None:
            self.tempo_fim = time.time()
        
        tempo_total = self.tempo_fim - self.tempo_inicio
        
        # Calcular médias
        media_poluicao = (self.poluicao_total / self.pontos_contados) if self.pontos_contados > 0 else 0
        media_densidade_pop = (self.densidade_pop_total / self.pontos_contados) if self.pontos_contados > 0 else 0
        media_areas_verdes = (self.areas_verdes_total / self.pontos_contados) if self.pontos_contados > 0 else 0

        # Eficiência energética: Bateria consumida por distância (simplificado)
        eficiencia_energetica = (self.bateria_consumida / self.distancia_total) if self.distancia_total > 0 else 0

        self.estatisticas = {
            "Tipo de Missão": self.tipo,
            "Distância Total Percorrida": f"{self.distancia_total:.2f} unidades",
            "Tempo Total da Missão": f"{tempo_total:.2f} segundos",
            "Média da Poluição do Ar": f"{media_poluicao:.2f} AQI",
            "Média da Densidade Populacional Sobrevoada": f"{media_densidade_pop:.2f} hab/km²",
            "Média de Áreas Verdes Sobrevoada": f"{media_areas_verdes:.2f}%",
            "Eficiência Energética (Bateria/Unidade)": f"{eficiencia_energetica:.2f}%/unidade"
        }

    def gerar_relatorio(self):
        """Retorna as estatísticas da missão."""
        if self.tempo_fim is None:
            self.finalizar_missao() # Garante que as estatísticas sejam calculadas
        return self.estatisticas

    def __str__(self):
        return f"Missão '{self.tipo}' - {self.estatisticas['Tempo Total da Missão']} - {self.estatisticas['Distância Total Percorrida']}"

class Drone:
    """
    Representa um drone com identificação, modelo, nível de bateria e histórico de missões.
    Cada drone pode ter uma missão ativa e várias missões finalizadas.
    """
    def __init__(self, identificador: str, modelo: str):
        self.identificador = identificador
        self.modelo = modelo
        self.missoes = ListaEncadeada() # Histórico de missões finalizadas
        self.missao_ativa = None
        self.bateria = 100 # Nível inicial da bateria (0-100%)

    def iniciar_missao(self, tipo_missao: str):
        """Inicia uma nova missão, se não houver outra em andamento."""
        if self.missao_ativa:
            # Não é mais um print, mas um retorno para a GUI lidar com isso
            return "⚠️ Já existe uma missão em andamento. Finalize antes de iniciar outra."

        self.bateria = 100 # Reseta a bateria para nova missão
        self.missao_ativa = Missao(tipo_missao)
        return f"🚀 Missão '{tipo_missao}' iniciada com sucesso."

    def registrar_ponto_voo(self, x: int, y: int, environmental_data):
        """Registra um ponto de voo na missão ativa e consome bateria."""
        if not self.missao_ativa:
            return "❌ Nenhuma missão ativa para registrar ponto."
        
        # Consumir bateria ao registrar ponto/mover
        # Cada movimento consome uma pequena quantidade
        consumo = random.uniform(0.5, 2.0)
        self.bateria = max(0, self.bateria - consumo)

        self.missao_ativa.registrar_ponto(x, y, self.bateria, environmental_data)
        return "Ponto de voo registrado."

    def finalizar_missao(self):
        """Finaliza a missão ativa e a armazena no histórico."""
        if not self.missao_ativa:
            return "❌ Nenhuma missão ativa para finalizar."

        self.missao_ativa.finalizar_missao()
        self.missoes.inserir_final(self.missao_ativa)
        missao_finalizada_tipo = self.missao_ativa.tipo
        self.missao_ativa = None
        return f"✅ Missão '{missao_finalizada_tipo}' finalizada com sucesso."

    def __str__(self):
        return f"🛸 Drone {self.identificador} - Modelo: {self.modelo}"

# =========================================================================
# FIM DAS CLASSES TEMPORÁRIAS/ADAPTADAS
# =========================================================================

# 🔧 Configurações do mapa
LARGURA_MAPA = 17  # Largura do mapa em número de células
ALTURA_MAPA = 10   # Altura do mapa em número de células

class InterfaceDrone:
    """Interface gráfica principal do simulador de missão com drones."""

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Missão de Drones")
        
        # Definir um tamanho fixo para a janela
        TAMANHO_CELULA_BASE_ESTIMADO = 50 
        LARGURA_SIDEBAR = 300 
        ESPACO_EXTRA_VERTICAL_BOTOES = 400 # Aumentado para mais espaço
        ALTURA_TITULO = 60 

        self.root.geometry(
            f"{TAMANHO_CELULA_BASE_ESTIMADO * LARGURA_MAPA + LARGURA_SIDEBAR}x"
            f"{TAMANHO_CELULA_BASE_ESTIMADO * ALTURA_MAPA + ESPACO_EXTRA_VERTICAL_BOTOES + ALTURA_TITULO}"
        )
        self.root.resizable(False, False) # DESABILITA O REDIMENSIONAMENTO DA JANELA
        self.root.configure(bg="#2c3e50") # Cor de fundo principal da janela (Dark Blue/Grey)

        # Configurações de estilo para ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam') # Usando o tema 'clam' para um visual mais moderno

        # Estilo para os botões principais (Inicar, Auto, Finalizar, Relatórios)
        self.style.configure('TButton',
                             font=('Inter', 12, 'bold'),
                             background='#42A5F5', # Azul vibrante
                             foreground='white',
                             borderwidth=0,
                             focusthickness=0, # Remove o foco estranho
                             relief='flat', # Botão plano
                             padding=12, # Aumentar padding
                             bordercolor='#42A5F5')
        self.style.map('TButton',
                       background=[('active', '#1E88E5')], # Azul mais escuro ao passar o mouse
                       relief=[('pressed', 'groove')]) # Efeito de pressionado

        # Estilo para os botões de navegação (setas)
        self.style.configure('Arrow.TButton',
                             font=('Inter', 16, 'bold'), # Fonte um pouco maior
                             background='#66BB6A', # Verde suave
                             foreground='white',
                             borderwidth=0,
                             focusthickness=0,
                             relief='flat',
                             width=4, height=2) # Tamanho fixo para as setas
        self.style.map('Arrow.TButton',
                       background=[('active', '#43A047')], # Verde mais escuro
                       relief=[('pressed', 'groove')])

        # Estilo para labels e outras informações
        self.style.configure('TLabel',
                             font=('Inter', 10),
                             background='#212121', # Será ajustado abaixo para contrastar com fundos específicos
                             foreground='#E0E0E0') # Texto cinza claro para contraste
        self.style.configure('Heading.TLabel', # Estilo para títulos de seção
                             font=('Inter', 14, 'bold'),
                             background='#34495e',
                             foreground='white',
                             padding=5)

        # Estilo para Frames com relevo
        self.style.configure('TFrame', background='#34495e') # Cor de fundo dos frames (Darker Blue/Grey)

        # Configuração da barra de progresso (bateria)
        self.style.configure("green.Horizontal.TProgressbar", foreground='green', background='green', thickness=20)
        self.style.configure("orange.Horizontal.TProgressbar", foreground='orange', background='orange', thickness=20)
        self.style.configure("red.Horizontal.TProgressbar", foreground='red', background='red', thickness=20)


        # 🚁 Gerenciamento de Drones
        self.drones = {
            "DRN001": Drone("DRN001", "Phantom Vision"),
            "DRN002": Drone("DRN002", "Mavic Explorer")
        }
        self.drone_selecionado_id = "DRN001"
        self.drone = self.drones[self.drone_selecionado_id] # Drone ativo

        # Posição inicial do drone centralizada
        self.x, self.y = LARGURA_MAPA // 2, ALTURA_MAPA // 2 

        # Mapa de dados ambientais (preenchido uma vez na inicialização)
        self.environmental_map_data = {}
        self._initialize_environmental_map()

        # Frame principal para organizar o layout (duas colunas: mapa e barra lateral)
        self.main_frame = ttk.Frame(root, style='TFrame', padding=(20, 20, 20, 20), relief="flat") # Usando ttk.Frame
        self.main_frame.pack(expand=True, fill='both')

        # Título principal da aplicação
        self.title_label = ttk.Label(self.main_frame, text="Simulador de Missões de Drones",
                                     font=('Inter', 20, 'bold'), foreground='#E0E0E0', background='#2c3e50') # Fundo do título = fundo da janela
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)


        # Frame para o mapa
        self.map_frame = ttk.Frame(self.main_frame, style='TFrame', padding=15)
        self.map_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew") # Coluna 0, abaixo do título
        self.main_frame.grid_rowconfigure(1, weight=1)

        # 🎨 Canvas do mapa
        self.canvas = tk.Canvas(
            self.map_frame,
            bg="#FFFFFF", # Fundo do canvas BRANCO
            bd=0, relief="flat", highlightthickness=0 # Remove borda padrão do canvas
        )
        self.canvas.pack(expand=True, fill='both')
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Button-1>", self.on_map_click) # Bind para clique na célula


        # Frame para a BARRA LATERAL (contém legenda, seleção de drone, telemetria e botões)
        self.sidebar_frame = ttk.Frame(self.main_frame, style='TFrame', padding=15)
        self.sidebar_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nswe")
        
        self.sidebar_frame.grid_rowconfigure(0, weight=0) # Legenda
        self.sidebar_frame.grid_rowconfigure(1, weight=0) # Seleção de Drone
        self.sidebar_frame.grid_rowconfigure(2, weight=0) # Telemetria
        self.sidebar_frame.grid_rowconfigure(3, weight=1) # Botões (expandem verticalmente)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        # 📘 Legenda da poluição (dentro da sidebar_frame)
        self.legenda = tk.Canvas(self.sidebar_frame, width=220, height=200, bg="#FFFFFF", bd=0, relief="flat", highlightthickness=0) # Fundo da legenda BRANCO
        self.legenda.grid(row=0, column=0, pady=(0, 20), sticky="n")
        self.desenhar_legenda()

        # Seleção de Drone
        self.drone_select_frame = ttk.Frame(self.sidebar_frame, style='TFrame', padding=5)
        self.drone_select_frame.grid(row=1, column=0, pady=(0, 15), sticky="ew")
        
        # A Tabela de label padrão tem um fundo escuro, sobrescrevendo-o aqui para o frame azul
        ttk.Label(self.drone_select_frame, text="Selecionar Drone:", font=('Inter', 10), background='#34495e', foreground='#E0E0E0').pack(pady=2)
        self.drone_combobox = ttk.Combobox(self.drone_select_frame, 
                                           values=list(self.drones.keys()), 
                                           state="readonly",
                                           font=('Inter', 10))
        self.drone_combobox.set(self.drone_selecionado_id)
        self.drone_combobox.bind("<<ComboboxSelected>>", self.on_drone_select)
        self.drone_combobox.pack(pady=5, fill='x', expand=True)

        # Painel de Telemetria
        self.telemetry_frame = ttk.Frame(self.sidebar_frame, style='TFrame', padding=10)
        self.telemetry_frame.grid(row=2, column=0, pady=(0, 15), sticky="ew")

        ttk.Label(self.telemetry_frame, text="Status do Drone", style='Heading.TLabel').pack(pady=5)
        self.telemetry_labels = {}
        telemetry_fields = ["Bateria", "Altitude", "Velocidade", "Vento", "Carga", "Câmera", "Fotos"]
        for field in telemetry_fields:
            # Sobrescrevendo o fundo do TLabel para combinar com o fundo do telemetry_frame
            label = ttk.Label(self.telemetry_frame, text=f"{field}: N/A", font=('Inter', 10), background='#34495e', foreground='#E0E0E0')
            label.pack(anchor="w", padx=5, pady=1)
            self.telemetry_labels[field] = label
        
        # Barra de progresso da bateria
        self.battery_progressbar = ttk.Progressbar(self.telemetry_frame, 
                                                   orient="horizontal", 
                                                   length=200, 
                                                   mode="determinate",
                                                   style="green.Horizontal.TProgressbar")
        self.battery_progressbar.pack(pady=10, fill='x', padx=5)

        # Frame para os BOTÕES DE CONTROLE
        self.control_buttons_frame = ttk.Frame(self.sidebar_frame, style='TFrame', padding=(0, 10, 0, 10))
        self.control_buttons_frame.grid(row=3, column=0, pady=10, sticky="ew")
        
        self.control_buttons_frame.grid_columnconfigure(0, weight=1)

        self.botao_iniciar = ttk.Button(self.control_buttons_frame, text="Iniciar Missão", command=self.iniciar_missao)
        self.botao_iniciar.grid(row=0, column=0, pady=5, sticky="ew")

        self.botao_auto = ttk.Button(self.control_buttons_frame, text="Simulação Automática", command=self.simular_movimento_automatico)
        self.botao_auto.grid(row=1, column=0, pady=5, sticky="ew")

        self.botao_finalizar = ttk.Button(self.control_buttons_frame, text="Finalizar Missão", command=self.finalizar_missao)
        self.botao_finalizar.grid(row=2, column=0, pady=5, sticky="ew")
        
        self.botao_exibir_relatorios = ttk.Button(self.control_buttons_frame, text="Exibir Relatórios de Missões", command=self.exibir_relatorio)
        self.botao_exibir_relatorios.grid(row=3, column=0, pady=10, sticky="ew")


        # Frame para os botões de navegação
        self.nav_buttons_frame = ttk.Frame(self.control_buttons_frame, style='TFrame', padding=10)
        self.nav_buttons_frame.grid(row=4, column=0, pady=(20, 5), sticky="ew")
        
        self.nav_buttons_frame.grid_columnconfigure(0, weight=1)
        self.nav_buttons_frame.grid_columnconfigure(1, weight=1)
        self.nav_buttons_frame.grid_columnconfigure(2, weight=1)

        self.botao_cima = ttk.Button(self.nav_buttons_frame, text="↑", command=lambda: self.mover_drone(0, -1), style='Arrow.TButton')
        self.botao_cima.grid(row=0, column=1, padx=5, pady=5)

        self.botao_esquerda = ttk.Button(self.nav_buttons_frame, text="←", command=lambda: self.mover_drone(-1, 0), style='Arrow.TButton')
        self.botao_esquerda.grid(row=1, column=0, padx=5, pady=5)

        self.botao_direita = ttk.Button(self.nav_buttons_frame, text="→", command=lambda: self.mover_drone(1, 0), style='Arrow.TButton')
        self.botao_direita.grid(row=1, column=2, padx=5, pady=5)

        self.botao_baixo = ttk.Button(self.nav_buttons_frame, text="↓", command=lambda: self.mover_drone(0, 1), style='Arrow.TButton')
        self.botao_baixo.grid(row=2, column=1, padx=5, pady=5)
        
        # Estas chamadas agora são feitas após a inicialização completa do objeto
        self.on_canvas_resize(None) # Desenha o mapa e atualiza telemetria inicial
        self.update_telemetry_display() # Atualiza telemetria inicial


    def _initialize_environmental_map(self):
        """Inicializa os dados ambientais para cada célula do mapa."""
        for r in range(ALTURA_MAPA):
            for c in range(LARGURA_MAPA):
                # Gerar dados ambientais aleatórios para cada célula
                env_data = {
                    "tipo_area": random.choice(["urbana", "residencial", "industrial", "rural", "mata", "zona de risco"]),
                    "densidade_populacional": random.randint(10, 5000), # Mais variado
                    "presenca_areas_verdes": random.randint(0, 100),
                    "indice_poluicao_ar": random.randint(1, 350),
                    "presenca_construcoes_altas": random.choice(["sim", "não"]),
                    "sinal_gps": random.choice(["forte", "fraco", "perdido"]),
                    "intensidade_ruido": random.randint(30, 100)
                }
                # Garante que dados específicos de área influenciem outros
                if env_data["tipo_area"] == "mata":
                    env_data["presenca_areas_verdes"] = random.randint(70, 100)
                    env_data["densidade_populacional"] = random.randint(1, 10)
                    env_data["presenca_construcoes_altas"] = "não"
                    env_data["indice_poluicao_ar"] = random.randint(10, 50)
                elif env_data["tipo_area"] == "industrial":
                    env_data["indice_poluicao_ar"] = random.randint(150, 350)
                    env_data["presenca_construcoes_altas"] = random.choice(["sim", "sim", "não"])
                    env_data["densidade_populacional"] = random.randint(50, 500)
                elif env_data["tipo_area"] == "zona de risco":
                    env_data["indice_poluicao_ar"] = random.randint(100, 250)
                    env_data["sinal_gps"] = random.choice(["fraco", "perdido"])
                    env_data["intensidade_ruido"] = random.randint(80, 120)

                self.environmental_map_data[(c, r)] = env_data # Armazena por coordenadas (coluna, linha)


    def on_drone_select(self, event):
        """Atualiza o drone ativo quando um novo é selecionado no combobox."""
        selected_id = self.drone_combobox.get()
        if selected_id in self.drones:
            self.drone_selecionado_id = selected_id
            self.drone = self.drones[selected_id]
            self.x, self.y = LARGURA_MAPA // 2, ALTURA_MAPA // 2 # Reposiciona o drone no centro para o novo drone
            self.desenhar_mapa()
            self.update_telemetry_display() # Atualiza a telemetria para o novo drone
            messagebox.showinfo("Drone Selecionado", f"Drone '{selected_id}' selecionado com sucesso.")


    def on_canvas_resize(self, event):
        """Redesenha o mapa quando o canvas é redimensionado."""
        self.desenhar_mapa()

    def on_map_click(self, event):
        """Exibe detalhes da célula clicada."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        cell_size_w = canvas_width / LARGURA_MAPA
        cell_size_h = canvas_height / ALTURA_MAPA
        current_cell_size = min(cell_size_w, cell_size_h)

        offset_x = (canvas_width - (current_cell_size * LARGURA_MAPA)) / 2
        offset_y = (canvas_height - (current_cell_size * ALTURA_MAPA)) / 2

        # Calcular as coordenadas da célula clicada
        clicked_col = int((event.x - offset_x) / current_cell_size)
        clicked_row = int((event.y - offset_y) / current_cell_size)

        if 0 <= clicked_col < LARGURA_MAPA and 0 <= clicked_row < ALTURA_MAPA:
            self.show_cell_details(clicked_col, clicked_row)
        else:
            messagebox.showinfo("Informação", "Clique dentro dos limites do mapa.")


    def show_cell_details(self, col, row):
        """Exibe uma nova janela com detalhes da célula clicada."""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Detalhes da Célula ({col}, {row})")
        details_window.transient(self.root)
        details_window.grab_set()
        details_window.resizable(False, False)
        details_window.configure(bg="#2c3e50") # Fundo da janela de detalhes azul/cinza

        details_frame = ttk.Frame(details_window, style='TFrame', padding=20)
        details_frame.pack(expand=True, fill='both')

        # Dados Ambientais
        ttk.Label(details_frame, text="Dados Ambientais:", style='Heading.TLabel').pack(pady=5, anchor="w")
        env_data = self.environmental_map_data.get((col, row), {})
        if env_data:
            for key, value in env_data.items():
                # Formatar chaves para exibição
                display_key = key.replace('_', ' ').title()
                if "populacional" in key:
                    display_value = f"{value} hab/km²"
                elif "areas_verdes" in key:
                    display_value = f"{value}%"
                elif "poluicao_ar" in key:
                    ponto_temp = PontoVoo(0,0,indice_poluicao_ar=value) # Usar PontoVoo para categoria
                    display_value = f"{value} ({ponto_temp.categoria_poluicao()[0]})"
                elif "ruido" in key:
                    display_value = f"{value} dB"
                else:
                    display_value = value
                # Fundo do TLabel para detalhes da célula combina com o frame azul
                ttk.Label(details_frame, text=f"- {display_key}: {display_value}", font=('Inter', 10), background='#34495e', foreground='#E0E0E0').pack(anchor="w", padx=10)
        else:
            ttk.Label(details_frame, text="Nenhum dado ambiental disponível.", font=('Inter', 10), background='#34495e', foreground='#E0E0E0').pack(anchor="w", padx=10)

        # Dados de Telemetria (se a célula foi visitada pelo drone ativo)
        if self.drone.missao_ativa:
            current_p_voo = None
            atual = self.drone.missao_ativa.pontos_voo.inicio
            while atual:
                if atual.dado.coordenadas == (col, row):
                    current_p_voo = atual.dado
                    break
                atual = atual.proximo
            
            if current_p_voo:
                ttk.Label(details_frame, text="\nDados de Telemetria (Última Visita):", style='Heading.TLabel').pack(pady=5, anchor="w")
                telemetry_dict = current_p_voo.to_dict()
                # Filtrar apenas os campos de telemetria
                telemetry_keys = ["Coordenadas", "Altitude", "Velocidade", "Direção do Vento", 
                                  "Nível da Bateria", "Temperatura Ambiente", "Status da Carga", 
                                  "Status da Câmera", "Fotos Registradas"]
                for key in telemetry_keys:
                    if key in telemetry_dict:
                        ttk.Label(details_frame, text=f"- {key}: {telemetry_dict[key]}", font=('Inter', 10), background='#34495e', foreground='#E0E0E0').pack(anchor="w", padx=10)
            else:
                ttk.Label(details_frame, text="\nCélula não visitada pelo drone atual.", font=('Inter', 10), background='#34495e', foreground='#E0E0E0').pack(pady=5, anchor="w")

        close_button = ttk.Button(details_frame, text="Fechar", command=details_window.destroy)
        close_button.pack(pady=15)


    def desenhar_legenda(self):
        """Desenha a legenda das categorias de poluição do ar."""
        categorias = [
            ("Ótima", "#00FF00"),       # Verde
            ("Moderada", "#FFFF00"),    # Amarelo
            ("Insalubre (sensíveis)", "#FFA500"), # Laranja
            ("Insalubre", "#FF0000"),   # Vermelho
            ("Muito insalubre", "#800080"), # Roxo
            ("Perigosa", "#8B0000")     # Vermelho Escuro
        ]
        self.legenda.delete("all")
        self.legenda.create_text(110, 15, text="Qualidade do Ar", font=("Inter", 13, "bold"), fill="black") # Texto preto na legenda branca
        self.legenda.create_line(10, 35, 210, 35, fill="#BDC3C7", width=1) # Separador mais claro

        for i, (label, cor) in enumerate(categorias):
            y = 50 + i * 25
            self.legenda.create_rectangle(20, y, 40, y + 20, fill=cor, outline="#BDC3C7", width=1) # Borda mais clara
            self.legenda.create_text(50, y + 10, anchor="w", text=label, font=("Inter", 10), fill="black") # Texto preto


    def desenhar_mapa(self):
        """Renderiza o mapa com o drone e os pontos visitados, ajustando o tamanho das células."""
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        cell_size_w = canvas_width / LARGURA_MAPA
        cell_size_h = canvas_height / ALTURA_MAPA
        
        self.current_cell_size = min(cell_size_w, cell_size_h) # Garante que células sejam quadradas

        # Calcular margens para centralizar o grid
        offset_x = (canvas_width - (self.current_cell_size * LARGURA_MAPA)) / 2
        offset_y = (canvas_height - (self.current_cell_size * ALTURA_MAPA)) / 2

        # Cor de fundo padrão das células
        default_cell_color = "#FFFFFF" # Cor de célula padrão BRANCA
        
        # Desenha as células do mapa e os pontos visitados
        for linha in range(ALTURA_MAPA):
            for coluna in range(LARGURA_MAPA):
                x0 = offset_x + coluna * self.current_cell_size
                y0 = offset_y + linha * self.current_cell_size
                x1 = x0 + self.current_cell_size
                y1 = y0 + self.current_cell_size

                cor_celula = default_cell_color

                # 🎯 Pintar com base na qualidade do ar se a célula foi visitada pelo drone ativo
                if self.drone.missao_ativa:
                    # Para a missão ativa, verifica os pontos visitados
                    atual = self.drone.missao_ativa.pontos_voo.inicio
                    is_visited_by_active_drone = False
                    while atual:
                        ponto = atual.dado
                        if ponto.coordenadas == (coluna, linha):
                            _, cor_poluicao = ponto.categoria_poluicao()
                            cor_celula = cor_poluicao # Usa a cor da poluição se visitada
                            is_visited_by_active_drone = True
                            break
                        atual = atual.proximo
                    
                    # Se não foi visitada pelo drone ATIVO, mantém a cor padrão do mapa
                    if not is_visited_by_active_drone:
                        cor_celula = default_cell_color
                else:
                    # Se não há missão ativa, todas as células são default_cell_color
                    cor_celula = default_cell_color


                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor_celula, outline="#BDC3C7", width=1) # Bordas cinza claro


        # Desenhar o caminho percorrido pelo drone (SE HOUVER UMA MISSÃO ATIVA)
        if self.drone.missao_ativa and not self.drone.missao_ativa.pontos_voo.esta_vazia():
            path_coords = []
            atual = self.drone.missao_ativa.pontos_voo.inicio
            while atual:
                px, py = atual.dado.coordenadas
                path_coords.append(offset_x + px * self.current_cell_size + self.current_cell_size / 2)
                path_coords.append(offset_y + py * self.current_cell_size + self.current_cell_size / 2)
                atual = atual.proximo
            
            if len(path_coords) >= 4: # Pelo menos 2 pontos para desenhar uma linha
                self.canvas.create_line(path_coords, fill="#3F51B5", width=3, smooth=True, tags="drone_path") # Azul escuro para o caminho
                self.canvas.tag_lower("drone_path") # Desenha o caminho abaixo do drone e das células

        # 🚁 Desenhar o drone na posição atual
        drone_x_center = offset_x + self.x * self.current_cell_size + self.current_cell_size / 2
        drone_y_center = offset_y + self.y * self.current_cell_size + self.current_cell_size / 2
        
        drone_size_factor = 0.6 # Fator para o tamanho do drone em relação à célula
        drone_width = self.current_cell_size * drone_size_factor
        drone_height = self.current_cell_size * drone_size_factor

        self.canvas.create_oval(
            drone_x_center - drone_width/2,
            drone_y_center - drone_height/2,
            drone_x_center + drone_width/2,
            drone_y_center + drone_height/2,
            fill="#FF5722", # Laranja/Vermelho vibrante
            outline="#D84315", # Mais escuro
            width=2,
            tags="drone"
        )
        # Adiciona um pequeno círculo no centro como indicador ou "câmera"
        self.canvas.create_oval(
            drone_x_center - drone_width/6,
            drone_y_center - drone_height/6,
            drone_x_center + drone_width/6,
            drone_y_center + drone_height/6,
            fill="white",
            outline="#424242",
            width=1,
            tags="drone_eye"
        )

        # Traz o drone para a frente para que esteja sempre visível
        self.canvas.tag_raise("drone")
        self.canvas.tag_raise("drone_eye")


    def update_telemetry_display(self):
        """Atualiza os labels de telemetria no painel da sidebar."""
        current_drone_obj = self.drone
        current_mission = current_drone_obj.missao_ativa

        if current_mission and not current_mission.pontos_voo.esta_vazia():
            last_ponto = current_mission.pontos_voo.fim.dado
            self.telemetry_labels["Altitude"].config(text=f"Altitude: {last_ponto.altitude}m")
            self.telemetry_labels["Velocidade"].config(text=f"Velocidade: {last_ponto.velocidade} km/h")
            self.telemetry_labels["Vento"].config(text=f"Vento: {last_ponto.direcao_vento}")
            self.telemetry_labels["Carga"].config(text=f"Carga: {last_ponto.status_carga}")
            self.telemetry_labels["Câmera"].config(text=f"Câmera: {last_ponto.status_camera}")
            self.telemetry_labels["Fotos"].config(text=f"Fotos: {last_ponto.num_fotos_registradas}")
        else:
            # Reseta os valores se não houver missão ativa ou pontos
            self.telemetry_labels["Altitude"].config(text="Altitude: N/A")
            self.telemetry_labels["Velocidade"].config(text="Velocidade: N/A")
            self.telemetry_labels["Vento"].config(text="Vento: N/A")
            self.telemetry_labels["Carga"].config(text="Carga: N/A")
            self.telemetry_labels["Câmera"].config(text="Câmera: N/A")
            self.telemetry_labels["Fotos"].config(text="Fotos: N/A")
        
        # Atualiza a bateria e a barra de progresso
        self.telemetry_labels["Bateria"].config(text=f"Bateria: {current_drone_obj.bateria:.1f}%")
        self.battery_progressbar['value'] = current_drone_obj.bateria

        # Mudar a cor da barra de progresso da bateria
        if current_drone_obj.bateria > 50:
            self.battery_progressbar.configure(style="green.Horizontal.TProgressbar")
        elif 20 <= current_drone_obj.bateria <= 50:
            self.battery_progressbar.configure(style="orange.Horizontal.TProgressbar")
        else:
            self.battery_progressbar.configure(style="red.Horizontal.TProgressbar")


    def iniciar_missao(self):
        """Solicita tipo e inicia uma nova missão."""
        # A mensagem agora vem do método do drone
        response = self.drone.iniciar_missao("") # Passa string vazia, pois o tipo é perguntado abaixo
        if "⚠️" in response: # Se já tem missão, mostra o aviso e sai
            messagebox.showwarning("Aviso", response)
            return

        tipo = simpledialog.askstring("Tipo de Missão", "Digite o tipo da missão:", parent=self.root)
        if not tipo:
            # Se o usuário cancelar, garante que a missão não seja iniciada de fato
            self.drone.missao_ativa = None 
            return

        # Agora realmente inicia com o tipo escolhido
        self.drone.iniciar_missao(tipo) # Chama de novo com o tipo
        self.x, self.y = LARGURA_MAPA // 2, ALTURA_MAPA // 2 # Resetar posição inicial
        
        # Obter os dados ambientais da célula inicial
        env_data_start = self.environmental_map_data.get((self.x, self.y), {})
        self.drone.registrar_ponto_voo(self.x, self.y, env_data_start)
        
        self.desenhar_mapa()
        self.update_telemetry_display()
        messagebox.showinfo("Sucesso", f"Missão '{tipo}' iniciada com sucesso para o Drone {self.drone.identificador}.")


    def mover_drone(self, dx, dy):
        """Move manualmente o drone na direção escolhida."""
        print(f"Debug: mover_drone chamado. dx={dx}, dy={dy}") # DEBUG: Confirma a chamada
        if self.drone.missao_ativa is None:
            messagebox.showwarning("Erro", "Inicie uma missão primeiro!")
            print("Debug: Nenhuma missão ativa.") # DEBUG
            return
        
        if self.drone.bateria <= 0:
            messagebox.showerror("Bateria Esgotada", "O drone ficou sem bateria e não pode se mover!")
            self.finalizar_missao() # Finaliza a missão se a bateria acabar
            print("Debug: Bateria esgotada.") # DEBUG
            return

        novo_x = self.x + dx
        novo_y = self.y + dy

        if 0 <= novo_x < LARGURA_MAPA and 0 <= novo_y < ALTURA_MAPA:
            self.x = novo_x
            self.y = novo_y
            print(f"Debug: Drone movido para ({self.x}, {self.y})") # DEBUG
            
            # Obter os dados ambientais da nova célula
            env_data = self.environmental_map_data.get((self.x, self.y), {})
            self.drone.registrar_ponto_voo(self.x, self.y, env_data) # Passa os dados ambientais
            self.desenhar_mapa()
            self.update_telemetry_display() # Atualiza a telemetria após o movimento
        else:
            messagebox.showwarning("Movimento inválido", "O drone não pode sair do mapa.")
            print("Debug: Movimento inválido (fora dos limites).") # DEBUG

    def simular_movimento_automatico(self):
        """Faz o drone se mover automaticamente por alguns passos."""
        if self.drone.missao_ativa is None:
            messagebox.showwarning("Erro", "Inicie uma missão primeiro!")
            return
        
        if self.drone.bateria <= 0:
            messagebox.showerror("Bateria Esgotada", "O drone ficou sem bateria e não pode se mover automaticamente!")
            self.finalizar_missao()
            return

        passos = 15 # Aumentei os passos para uma simulação mais longa
        
        def _auto_move_step(step_count):
            if step_count >= passos or self.drone.bateria <= 0:
                if self.drone.bateria <= 0:
                    messagebox.showerror("Bateria Esgotada", "A simulação automática foi interrompida: bateria esgotada!")
                    self.finalizar_missao()
                else:
                    messagebox.showinfo("Simulação Concluída", "A simulação automática terminou os passos definidos.")
                return

            direcao = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)]) # Cima, Baixo, Esquerda, Direita
            novo_x = self.x + direcao[0]
            novo_y = self.y + direcao[1]

            if 0 <= novo_x < LARGURA_MAPA and 0 <= novo_y < ALTURA_MAPA:
                self.x = novo_x
                self.y = novo_y
                env_data = self.environmental_map_data.get((self.x, self.y), {})
                self.drone.registrar_ponto_voo(self.x, self.y, env_data)
                self.desenhar_mapa()
                self.update_telemetry_display()
                # Agenda o próximo passo
                self.root.after(250, lambda: _auto_move_step(step_count + 1))
            else:
                # Se bater na borda, tenta o próximo passo imediatamente sem mover
                _auto_move_step(step_count + 1)

        _auto_move_step(0) # Inicia a simulação automática


    def finalizar_missao(self):
        """Finaliza a missão ativa e exibe relatório."""
        response = self.drone.finalizar_missao()
        messagebox.showinfo("Missão Finalizada", response)
        self.desenhar_mapa() # Atualiza o mapa após finalizar
        self.update_telemetry_display() # Reseta a telemetria
        self.exibir_relatorio() # Exibe todos os relatórios


    def exibir_relatorio(self):
        """Mostra relatórios de todas as missões do drone selecionado em uma nova janela."""
        relatorios = []
        atual = self.drone.missoes.inicio
        if not atual:
            messagebox.showinfo("Relatório", "Nenhum relatório disponível para este drone.")
            return

        while atual:
            relatorio = atual.dado.gerar_relatorio()
            texto = ""
            for k, v in relatorio.items():
                texto += f"- {k}: {v}\n"
            relatorios.append(texto)
            atual = atual.proximo

        if relatorios:
            report_window = tk.Toplevel(self.root)
            report_window.title(f"Relatórios de Missões - Drone {self.drone.identificador}")
            report_window.transient(self.root)
            report_window.grab_set()
            report_window.resizable(False, False)
            report_window.configure(bg="#2c3e50") # Fundo da janela de relatório azul/cinza

            report_frame = ttk.Frame(report_window, style='TFrame', padding=20)
            report_frame.pack(expand=True, fill='both')

            # Título do relatório
            ttk.Label(report_frame, text=f"Histórico de Missões do {self.drone.identificador}",
                      font=('Inter', 16, 'bold'), foreground='#E0E0E0', background='#34495e').pack(pady=(0, 15))


            # Usar um Text widget com Scrollbar para múltiplos relatórios
            text_scroll_frame = ttk.Frame(report_frame, style='TFrame')
            text_scroll_frame.pack(expand=True, fill='both')

            report_text = tk.Text(text_scroll_frame, wrap="word", bg="#FFFFFF", fg="black", # Fundo do texto BRANCO, texto PRETO
                                  font=('Inter', 10), bd=0, relief="flat", padx=10, pady=10)
            report_text.pack(side=tk.LEFT, expand=True, fill='both')

            scrollbar = ttk.Scrollbar(text_scroll_frame, command=report_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill='y')
            report_text.config(yscrollcommand=scrollbar.set)

            # Insere todos os relatórios
            for i, rel in enumerate(relatorios):
                report_text.insert(tk.END, f"\n--- Missão {i+1} ---\n", "mission_header")
                report_text.insert(tk.END, rel + "\n")
            
            report_text.tag_configure("mission_header", font=('Inter', 12, 'bold'), foreground='#42A5F5')
            report_text.config(state=tk.DISABLED) # Torna o texto somente leitura

            close_button = ttk.Button(report_frame, text="Fechar", command=report_window.destroy)
            close_button.pack(pady=10)


def iniciar_interface():
    """Função para iniciar a interface gráfica."""
    root = tk.Tk()
    app = InterfaceDrone(root)
    root.mainloop()
