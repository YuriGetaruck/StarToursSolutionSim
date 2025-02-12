from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d import Axes3D
from fpdf import FPDF
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import threading
import os
import platform
import time
import csv


class AnimatedGraphApp:
    def __init__(self, root):

        self.caminho = [0, 3, 1, 2, 4, 7, 23, 41, 16, 9, 28, 40, 38, 35, 66, 75, 91, 86, 46, 64, 44, 77, 82, 69, 63, 55, 45, 31, 27, 20, 59, 74, 76, 68, 56, 12, 11, 24, 17, 43, 84, 70, 52, 51, 81, 60, 78, 39, 37, 5, 10, 34, 48, 50, 85, 79, 80, 65, 62, 36, 25, 29, 67, 89, 33, 53, 49, 94, 92, 88, 15, 21, 26, 6, 22, 8, 19, 18, 
30, 99, 95, 98, 42, 54, 57, 72, 61, 73, 87, 97, 13, 14, 32, 58, 93, 83, 71, 96, 90, 47, 0]
        self.distancia_caminho = self.calcula_distancia_caminho()
        self.distancia_o = self.get_distancia_otima()
        self.prox_caminho_o = self.get_prox_caminho_o()
        self.tempo_execucao = 0;
        self.root = root
        self.root.title("Simulador StarTours - Yuri Getaruck")
        ctk.set_appearance_mode("dark")  # Modo escuro
        ctk.set_default_color_theme("dark-blue")  # Tema azul escuro

        # Definir o tamanho da janela para Full HD
        self.root.geometry("1600x918")  # ratio 400:217
        self.root.resizable(False, False)  # Impedir redimensionamento (largura e altura)

        # Configuração do layout
        self.frame_left = ctk.CTkFrame(self.root)
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.frame_middle = ctk.CTkFrame(self.root)
        self.frame_middle.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_middle.configure(fg_color="black")

        self.frame_right = ctk.CTkFrame(self.root)
        self.frame_right.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Parâmetros de customização
        self.param_label = ctk.CTkLabel(self.frame_left, text="Parâmetros de Customização")
        self.param_label.pack(pady=5)

        self.algoritmo_label = ctk.CTkLabel(self.frame_left, text="Algoritmo:")
        self.algoritmo_label.pack(pady=5)
        self.algoritmo_var = ctk.StringVar(value="Nearest Neighbor (NN)")
        self.algoritmo_select = ctk.CTkComboBox(self.frame_left, variable=self.algoritmo_var, values=["Nearest Neighbor (NN)", "Genetic Algorithm (GA)", "Ant Colony Optimization (ACO)", "Greedy Randomized Adaptive Search Procedure (GRASP)"], command=self.on_algoritmo_select)
        self.algoritmo_select.pack(pady=5)

        self.dataset_label = ctk.CTkLabel(self.frame_left, text="Dataset:")
        self.dataset_label.pack(pady=5)
        self.dataset_var = ctk.StringVar(value="100 Estrelas")
        self.dataset_select = ctk.CTkComboBox(self.frame_left, variable=self.dataset_var, values=["100 Estrelas", "1.000 Estrelas", "10.000 Estrelas", "37.859 Estrelas", "109.399 Estrelas"])
        self.dataset_select.pack(pady=5)

        # Hiperparâmetros para Algoritmo Genético
        self.mutacao_label = ctk.CTkLabel(self.frame_left, text="Taxa de Mutação:")
        self.mutacao_label.pack(pady=5)
        self.mutacao_slider = ctk.CTkSlider(self.frame_left, from_=0.00, to=1.00, number_of_steps=100, command=self.update_mutacao, width=150)
        self.mutacao_slider.pack(pady=5)
        self.mutacao_var = ctk.StringVar(value="0.15")
        self.mutacao_entry = ctk.CTkEntry(self.frame_left, textvariable=self.mutacao_var)
        self.mutacao_entry.pack(pady=5)

        self.populacao_label = ctk.CTkLabel(self.frame_left, text="Tamanho da População:")
        self.populacao_label.pack(pady=5)
        self.populacao_var = ctk.StringVar(value="250")
        self.populacao_entry = ctk.CTkEntry(self.frame_left, textvariable=self.populacao_var)
        self.populacao_entry.pack(pady=5)

        self.iteracoes_label = ctk.CTkLabel(self.frame_left, text="Número de Iterações:")
        self.iteracoes_label.pack(pady=5)
        self.iteracoes_var = ctk.StringVar(value="7000")
        self.iteracoes_entry = ctk.CTkEntry(self.frame_left, textvariable=self.iteracoes_var)
        self.iteracoes_entry.pack(pady=5)

        # Hiperparâmetros para Algoritmo de Colônia de Formigas (ACO)
        self.n_ants_label = ctk.CTkLabel(self.frame_left, text="Número de Formigas:")
        self.n_ants_label.pack(pady=5)
        self.n_ants_var = ctk.StringVar(value="100")  # Cria um StringVar com o valor padrão
        self.n_ants_entry = ctk.CTkEntry(self.frame_left, textvariable=self.n_ants_var)
        self.n_ants_entry.pack(pady=5)

        self.n_iterations_label = ctk.CTkLabel(self.frame_left, text="Número de Iterações:")
        self.n_iterations_label.pack(pady=5)
        self.n_iterations_var = ctk.StringVar(value="50")  # Cria um StringVar com o valor padrão
        self.n_iterations_entry = ctk.CTkEntry(self.frame_left, textvariable=self.n_iterations_var)
        self.n_iterations_entry.pack(pady=5)

        self.alpha_label = ctk.CTkLabel(self.frame_left, text="Valor de Alpha:")
        self.alpha_label.pack(pady=5)
        self.alpha_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=3.0, number_of_steps=100, command=self.update_alpha, width=150)
        self.alpha_slider.pack(pady=5)
        self.alpha_var = ctk.StringVar(value="1.60")
        self.alpha_entry = ctk.CTkEntry(self.frame_left, textvariable=self.alpha_var)
        self.alpha_entry.pack(pady=5)

        self.beta_label = ctk.CTkLabel(self.frame_left, text="Valor de Beta:")
        self.beta_label.pack(pady=5)
        self.beta_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=5.0, number_of_steps=100, command=self.update_beta, width=150)
        self.beta_slider.pack(pady=5)
        self.beta_var = ctk.StringVar(value="2.00")
        self.beta_entry = ctk.CTkEntry(self.frame_left, textvariable=self.beta_var)
        self.beta_entry.pack(pady=5)

        self.evaporation_label = ctk.CTkLabel(self.frame_left, text="Taxa de Evaporação:")
        self.evaporation_label.pack(pady=5)
        self.evaporation_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=1.0, number_of_steps=100, command=self.update_evaporation, width=150)
        self.evaporation_slider.pack(pady=5)
        self.evaporation_var = ctk.StringVar(value="0.70")
        self.evaporation_entry = ctk.CTkEntry(self.frame_left, textvariable=self.evaporation_var)
        self.evaporation_entry.pack(pady=5)

        self.q_label = ctk.CTkLabel(self.frame_left, text="Valor de Q:")
        self.q_label.pack(pady=5)
        self.q_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=10.0, number_of_steps=100, command=self.update_q, width=150)
        self.q_slider.pack(pady=5)
        self.q_var = ctk.StringVar(value="15.00")
        self.q_entry = ctk.CTkEntry(self.frame_left, textvariable=self.q_var)
        self.q_entry.pack(pady=5)

        # Hiperparâmetros para GRASP
        self.grasp_alpha_label = ctk.CTkLabel(self.frame_left, text="Alpha:")
        self.grasp_alpha_label.pack(pady=5)
        self.grasp_alpha_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=1.0, number_of_steps=100, command=self.update_grasp_alpha, width=150)
        self.grasp_alpha_slider.pack(pady=5)
        self.grasp_alpha_var = ctk.StringVar(value="0.25")
        self.grasp_alpha_entry = ctk.CTkEntry(self.frame_left, textvariable=self.grasp_alpha_var)
        self.grasp_alpha_entry.pack(pady=5)

        self.grasp_iterations_label = ctk.CTkLabel(self.frame_left, text="Número de Iterações:")
        self.grasp_iterations_label.pack(pady=5)
        self.grasp_iterations_var = ctk.StringVar(value="4000")  # Cria um StringVar com o valor padrão
        self.grasp_iterations_entry = ctk.CTkEntry(self.frame_left, textvariable=self.grasp_iterations_var)
        self.grasp_iterations_entry.pack(pady=5)

        # Botão para plotar o melhor caminho
        self.plot_best_path_checkbox = ctk.CTkCheckBox(self.frame_left, text="Plotar Melhor Caminho", command=self.plot_best_path_checkbox_command)
        self.plot_best_path_checkbox.pack(pady=20)
        
        # Inicialmente, ocultar os parâmetros
        self.toggle_ga_params(False)
        self.toggle_aco_params(False)
        self.toggle_grasp_params(False)
        
        # Botao Run
        self.run_button = ctk.CTkButton(self.frame_left, text="RUN", command=self.run_algoritmo)
        self.run_button.pack(pady=20)

        # Seção de Resultados
        self.result_label = ctk.CTkLabel(self.frame_right, text="Resultados")
        self.result_label.pack(pady=5)
        
        self.distancia_label = ctk.CTkLabel(self.frame_right, text="Distância Total:")
        self.distancia_label.pack(pady=5)
        self.distancia_text = ctk.CTkTextbox(self.frame_right, height=10, width=150)
        self.distancia_text.pack(pady=5)
        self.distancia_text.insert(ctk.END, f"{self.distancia_caminho:.2f}")

        self.distancia_o_label = ctk.CTkLabel(self.frame_right, text="Distância Ótima:")
        self.distancia_o_label.pack(pady=5)
        self.distancia_o_text = ctk.CTkTextbox(self.frame_right, height=10, width=150)
        self.distancia_o_text.pack(pady=5)
        self.distancia_o_text.insert(ctk.END, f"{self.distancia_o:.2f}")

        self.proximidade_caminho_o_label = ctk.CTkLabel(self.frame_right, text="Proximidade caminho ótimo:")
        self.proximidade_caminho_o_label.pack(pady=5)
        self.proximidade_caminho_o_text = ctk.CTkTextbox(self.frame_right, height=10, width=150)
        self.proximidade_caminho_o_text.pack(pady=5)
        self.proximidade_caminho_o_text.insert(ctk.END, f"{self.prox_caminho_o:.2f} %")

        self.progress_label = ctk.CTkLabel(self.frame_right, text="Progresso do Algoritmo: ", font=("Arial", 16))
        self.progress_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.frame_right, width=300)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

        self.progress_percentage = ctk.CTkLabel(self.frame_right, text="0%", font=("Arial", 14))
        self.progress_percentage.pack(pady=10)

        self.proximidade_caminho_o_label = ctk.CTkLabel(self.frame_right, text="Tempo execução:")
        self.proximidade_caminho_o_label.pack(pady=5)
        self.tempo_execucao_text = ctk.CTkTextbox(self.frame_right, height=10, width=150)
        self.tempo_execucao_text.pack(pady=5)
        self.tempo_execucao_text.insert(ctk.END, f"{self.tempo_execucao:.4f} segundos")
        
        # Configuração do gráfico 3D
        self.fig = plt.figure()
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.ax = self.fig.add_subplot(111, projection='3d')
        # Remover as bordas do gráfico
        self.ax.set_axis_off()

        # Ajuste das bordas do plot
        self.plota_caminho(self.caminho)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_middle)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

        # Configurar o protocolo de fechamento de janela
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
    
    def update_graph(self):
        # Limpar o gráfico atual
        self.ax.clear()
        self.ax.set_axis_off()

        
        # Plotar o novo caminho
        self.plota_caminho(self.caminho)
        
        # Atualizar o canvas com o novo gráfico
        self.canvas.draw()

        # self.caminho_text.delete("1.0", ctk.END)
        # self.caminho_text.insert(ctk.END, self.caminho)
        self.distancia_caminho = self.calcula_distancia_caminho()
        self.distancia_text.delete("1.0", ctk.END)
        self.distancia_text.insert(ctk.END, f"{self.distancia_caminho:.2f}")
        self.distancia_o = self.get_distancia_otima()
        self.distancia_o_text.delete("1.0", ctk.END)
        self.distancia_o_text.insert(ctk.END, f"{self.distancia_o:.2f}")
        self.prox_caminho_o = self.get_prox_caminho_o()
        self.proximidade_caminho_o_text.delete("1.0", ctk.END)
        self.proximidade_caminho_o_text.insert(ctk.END, f"{self.prox_caminho_o:.2f} %")
        self.tempo_execucao_text.delete("1.0", ctk.END)
        self.tempo_execucao_text.insert(ctk.END, f"{self.tempo_execucao:.4f} segundos")


    def get_distancia_otima(self):
        tam = len(self.caminho)
        match tam:
            case 101:
                return 1795
            case 1001:
                return 22227
            case 10001:
                return 276750
            case 37860:
                return 28235453 
            case 109400:
                return 13750874
            
    def get_prox_caminho_o(self):
        return (self.distancia_o/self.distancia_caminho) * 100
    
    def on_algoritmo_select(self, event=None):
        selected_algo = self.algoritmo_var.get()
        print(f"Algoritmo selecionado: {selected_algo}")  # Verificação de debug
        if selected_algo == "Genetic Algorithm (GA)":
            self.toggle_ga_params(True)
        else:
            self.toggle_ga_params(False)
        if selected_algo == "Ant Colony Optimization (ACO)":
            self.toggle_aco_params(True)
        else:
            self.toggle_aco_params(False)
        if selected_algo == "Greedy Randomized Adaptive Search Procedure (GRASP)":
            self.toggle_grasp_params(True)
        else:
            self.toggle_grasp_params(False)
        

    def toggle_ga_params(self, show):
        if show:
            self.mutacao_label.pack(pady=5)
            self.mutacao_slider.pack(pady=5)
            self.mutacao_entry.pack(pady=5)
            self.populacao_label.pack(pady=5)
            self.populacao_entry.pack(pady=5)
            self.iteracoes_label.pack(pady=5)
            self.iteracoes_entry.pack(pady=5)
        else:
            self.mutacao_label.pack_forget()
            self.mutacao_slider.pack_forget()
            self.mutacao_entry.pack_forget()
            self.populacao_label.pack_forget()
            self.populacao_entry.pack_forget()
            self.iteracoes_label.pack_forget()
            self.iteracoes_entry.pack_forget()

    def toggle_grasp_params(self, show):
        if show:
            self.grasp_alpha_label.pack(pady=5)
            self.grasp_alpha_slider.pack(pady=5)
            self.grasp_alpha_entry.pack(pady=5)
            self.grasp_iterations_label.pack(pady=5)
            self.grasp_iterations_entry.pack(pady=5)
        else:
            self.grasp_alpha_label.pack_forget()
            self.grasp_alpha_slider.pack_forget()
            self.grasp_alpha_entry.pack_forget()
            self.grasp_iterations_label.pack_forget()
            self.grasp_iterations_entry.pack_forget()

    def toggle_aco_params(self, show):
        if show:
            self.n_ants_label.pack(pady=5)
            self.n_ants_entry.pack(pady=5)
            self.n_iterations_label.pack(pady=5)
            self.n_iterations_entry.pack(pady=5)
            self.alpha_label.pack(pady=5)
            self.alpha_slider.pack(pady=5)
            self.alpha_entry.pack(pady=5)
            self.beta_label.pack(pady=5)
            self.beta_slider.pack(pady=5)
            self.beta_entry.pack(pady=5)
            self.evaporation_label.pack(pady=5)
            self.evaporation_slider.pack(pady=5)
            self.evaporation_entry.pack(pady=5)
            self.q_label.pack(pady=5)
            self.q_slider.pack(pady=5)
            self.q_entry.pack(pady=5)
        else:
            self.n_ants_label.pack_forget()
            self.n_ants_entry.pack_forget()
            self.n_iterations_label.pack_forget()
            self.n_iterations_entry.pack_forget()
            self.alpha_label.pack_forget()
            self.alpha_slider.pack_forget()
            self.alpha_entry.pack_forget()
            self.beta_label.pack_forget()
            self.beta_slider.pack_forget()
            self.beta_entry.pack_forget()
            self.evaporation_label.pack_forget()
            self.evaporation_slider.pack_forget()
            self.evaporation_entry.pack_forget()
            self.q_label.pack_forget()
            self.q_slider.pack_forget()
            self.q_entry.pack_forget()
        
    def update_mutacao(self, value):
        self.mutacao_var.set(f"{float(value):.2f}")

    def update_alpha(self, value):
        self.alpha_var.set(f"{float(value):.2f}")

    def update_grasp_alpha(self, value):
        self.grasp_alpha_var.set(f"{float(value):.2f}")

    def update_beta(self, value):
        self.beta_var.set(f"{float(value):.2f}")
    
    def update_evaporation(self, value):
        self.evaporation_var.set(f"{float(value):.2f}")

    def update_q(self, value):
        self.q_var.set(f"{float(value):.2f}")

    def plot_best_path_checkbox_command(self):
        if(self.plot_best_path_checkbox.get() == 1):
            dataset_tour = "star100_tour.txt"

            grossura_linha = 2
            
            match self.dataset_select.get():
                case "100 Estrelas":
                    dataset_tour = "star100_tour.txt"
                    dataset_name = "star100.xyz.txt"
                    grossura_linha = 2
                case "1.000 Estrelas":
                    dataset_tour = "star1k_tour.txt"
                    dataset_name = "star1k.xyz.txt"
                    grossura_linha = 2
                case "10.000 Estrelas":
                    dataset_tour = "star10k_tour.txt"
                    dataset_name = "star10k.xyz.txt"
                    grossura_linha = 1
                case "37.859 Estrelas":
                    dataset_tour = "kj37859_tour.txt"
                    dataset_name = "kj37859.xyz.txt"
                    grossura_linha = 0.5
                case "109.399 Estrelas":
                    dataset_tour = "hyg109399_tour.txt"
                    dataset_name = "hyg109399.xyz.txt"
                    grossura_linha = 0.1
        
            # Nome do arquivo do melhor caminho (alterar conforme necessário)
            best_path_file = "best_paths/" + dataset_tour
            
            # Carregar o melhor caminho do arquivo
            with open(best_path_file, 'r') as file:
                best_path = [int(line.strip()) for line in file]

            for i in range(len(best_path)):
                best_path[i] = best_path[i] - 1
            best_path.append(0)
            
            # Adicionar o melhor caminho ao gráfico
            self.ax.clear()
            self.ax.set_axis_off()
            
            # Plotar o caminho atual
            self.plota_caminho(self.caminho)
            
            # Plotar o melhor caminho
            tam = len(best_path)
            coordenadas_x = np.zeros(tam, dtype=float)
            coordenadas_y = np.zeros(tam, dtype=float)
            coordenadas_z = np.zeros(tam, dtype=float)
            
            # Assumindo que você já tem uma função para abrir o dataset
            coordenadas = self.open_dataset(os.path.join("datasets",dataset_name))  # Altere o nome do arquivo conforme necessário
            
            for i in range(tam):
                coordenadas_x[i] = coordenadas[best_path[i]][1]
                coordenadas_y[i] = coordenadas[best_path[i]][2]
                coordenadas_z[i] = coordenadas[best_path[i]][3]
            
            self.ax.plot(coordenadas_x, coordenadas_y, coordenadas_z, color='red', linewidth=grossura_linha)

            RADIUS = (max(coordenadas_x.max(), coordenadas_y.max(), coordenadas_z.max())) * 1.33

            self.ax.set_xlim3d(-RADIUS / 2, RADIUS / 2)
            self.ax.set_zlim3d(-RADIUS / 2, RADIUS / 2)
            self.ax.set_ylim3d(-RADIUS / 2, RADIUS / 2)

            # Atualizar o canvas com o novo gráfico
            self.canvas.draw()
        else:
            self.update_graph()

    def atualizar_barra_progresso(self, log_file, iteracoes_totais):
        def atualizar_barra_progresso_sub_process(log_file, iteracoes_totais):
            iteracao_atual = 0
            self.progress_bar.set(0)
            time.sleep(0.5)


            while iteracao_atual < int(iteracoes_totais):
                # Abrir o arquivo CSV e ler as linhas
                with open("c_scripts/logs/" + log_file + ".txt", "r") as file:
                    csv_reader = csv.reader(file)
                    last_row = None
                    for row in csv_reader:
                        last_row = row  # Mantém a última linha lida

                    if last_row:  # Se houver dados no CSV
                        iteracao_atual = int(last_row[0])  # Usar a primeira célula (iterações)

                # Atualizar a barra de progresso
                progresso = iteracao_atual / int(iteracoes_totais)
                self.progress_bar.set(progresso)
                self.progress_percentage.configure(text=f"{int(progresso * 100)}%")
                
                time.sleep(0.1)

        # Inicia a thread para atualizar a barra de progresso
        threading.Thread(target=atualizar_barra_progresso_sub_process, args=(log_file, iteracoes_totais)).start()
        
    def analisar_log_e_gerar_graficos(self, log_file: str, total_iteracoes: int, distancia_otima: float):
        # Variáveis para armazenar dados
        iteracoes = []
        distancias = []
        tempos = []

        time.sleep(2)

        # Leitura do arquivo CSV
        with open("c_scripts/logs/" + log_file + ".txt", "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                iteracao = int(row[0])  # Iteração
                distancia = float(row[1])  # Distância
                tempo = float(row[2])  # Tempo

                iteracoes.append(iteracao)
                distancias.append(distancia)
                tempos.append(tempo)
        
        # Calculando a distância mínima obtida
        distancia_obtida = np.min(distancias)

        # Calculando a Taxa de Melhoria e Taxa de Convergência
        taxa_melhoria = [100 * (distancia_otima - dist) / distancia_otima for dist in distancias]
        taxa_convergencia = [0] + [100 * (distancias[i - 1] - distancias[i]) / distancias[i - 1] for i in range(1, len(distancias))]

        # Gerar gráfico da Taxa de Melhoria
        plt.figure(figsize=(10, 5))
        plt.plot(iteracoes, taxa_melhoria, label="Taxa de Melhoria (%)", color="blue")
        plt.xlabel("Iterações")
        plt.ylabel("Taxa de Melhoria (%)")
        plt.title("Taxa de Melhoria ao Longo das Iterações")
        plt.legend()
        plt.grid(True)
        plt.savefig("taxa_melhoria.png")

        # Gerar gráfico da Taxa de Convergência
        plt.figure(figsize=(10, 5))
        plt.plot(iteracoes, taxa_convergencia, label="Taxa de Convergência (%)", color="green")
        plt.xlabel("Iterações")
        plt.ylabel("Taxa de Convergência (%)")
        plt.title("Taxa de Convergência ao Longo das Iterações")
        plt.legend()
        plt.grid(True)
        plt.savefig("taxa_convergencia.png")

        # Gerar gráfico da Distância Total
        plt.figure(figsize=(10, 5))
        plt.plot(iteracoes, distancias, label="Distância Total", color="purple")
        plt.axhline(y=distancia_otima, color="red", linestyle="--", label="Distância Ótima")
        plt.xlabel("Iterações")
        plt.ylabel("Distância Total")
        plt.title("Distância Total ao Longo das Iterações")
        plt.legend()
        plt.grid(True)
        plt.savefig("distancia_total.png")

        # Criando PDF com gráficos
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Análise de Log de Iterações", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Total de Iterações: {total_iteracoes}", ln=True, align="L")
        pdf.cell(200, 10, f"Distância Ótima: {distancia_otima}", ln=True, align="L")
        pdf.cell(200, 10, f"Distância Obtida: {distancia_obtida}", ln=True, align="L")
        pdf.cell(200, 10, f"Proximidade do caminho ótimo: {(distancia_otima / distancia_obtida) * 100:.2f}%", ln=True, align="L")
        pdf.cell(200, 10, f"Tempo de execução: {self.tempo_execucao:.2f} segundos", ln=True, align="L")

        pdf.add_page()
        pdf.image("taxa_melhoria.png", x=10, y=20, w=180)
        pdf.add_page()
        pdf.image("taxa_convergencia.png", x=10, y=20, w=180)
        pdf.add_page()
        pdf.image("distancia_total.png", x=10, y=20, w=180)

        # Salva o PDF
        pdf.output("analise_log.pdf")

        print("PDF 'analise_log.pdf' criado com sucesso.")


    def run_algoritmo(self):
        def run():
            # Lógica para chamar o código em C aqui
            self.run_button.configure(state="disabled")
            algoritmo = self.algoritmo_var.get()
            dataset = self.dataset_var.get()
            dataset_size = "100"
            dataset_name = "star100.xyz.txt"

            match dataset:
                case "100 Estrelas":
                    dataset_name = "star100.xyz.txt"
                    dataset_size = "100"
                case "1.000 Estrelas":
                    dataset_name = "star1k.xyz.txt"
                    dataset_size = "1000"
                case "10.000 Estrelas":
                    dataset_name = "star10k.xyz.txt"
                    dataset_size = "10000"
                case "37.859 Estrelas":
                    dataset_name = "kj37859.xyz.txt"
                    dataset_size = "37859"
                case "109.399 Estrelas":
                    dataset_name = "hyg109399.xyz.txt"
                    dataset_size = "109399"

            # Adiciona o sufixo exe ao arquivo binário caso esteja rodando no Windows
            bin_sulfix = ".exe" if platform.system() == "Windows" else ""

            match algoritmo:
                case "Nearest Neighbor (NN)":
                    algoritmo_sigla = "nn"
                    algoritmo = os.path.join("c_scripts", algoritmo_sigla + bin_sulfix)
                    args = [algoritmo, dataset_name, dataset_size]
                    iteracoes_selecionadas = int(dataset_size)
                case "Genetic Algorithm (GA)":
                    algoritmo_sigla = "ga"
                    algoritmo = os.path.join("c_scripts", algoritmo_sigla + bin_sulfix)
                    args = [algoritmo, dataset_name, dataset_size, self.mutacao_entry.get(), self.populacao_entry.get(), self.iteracoes_entry.get()]
                    iteracoes_selecionadas = self.iteracoes_entry.get()
                case "Ant Colony Optimization (ACO)":
                    algoritmo_sigla = "aco"
                    algoritmo = os.path.join("c_scripts", algoritmo_sigla + bin_sulfix)
                    args = [algoritmo, dataset_name, dataset_size, self.n_ants_entry.get(), self.n_iterations_entry.get(), self.alpha_entry.get(), self.beta_entry.get(), self.evaporation_entry.get(), self.q_entry.get()]
                    iteracoes_selecionadas = self.n_iterations_entry.get()
                case "Greedy Randomized Adaptive Search Procedure (GRASP)":
                    algoritmo_sigla = "grasp"
                    algoritmo = os.path.join("c_scripts", algoritmo_sigla + bin_sulfix)
                    args = [algoritmo, dataset_name, dataset_size, self.grasp_iterations_var.get(), self.grasp_alpha_var.get()]
                    iteracoes_selecionadas = self.grasp_iterations_var.get()

            print(f"algoritmo: {algoritmo} dataset: {dataset_name} dataset_size: {dataset_size}")

            # Inicia a contagem de tempo antes de chamar o processo
            start_time = time.time()

            # Executa o processo
            print(args)
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            match algoritmo_sigla:
                    case "grasp":
                        log_file = "log_grasp_" + dataset_size + "_" + self.grasp_alpha_var.get() + "_" + self.grasp_iterations_var.get()
                    case "aco":
                        log_file = "log_aco_" + dataset_size + "_" + self.n_ants_entry.get() + "_" + self.alpha_entry.get() + "_" + self.beta_entry.get() + "_" + self.evaporation_entry.get() + "_" + self.q_entry.get() + "_" + self.n_iterations_entry.get()
                    case "ga":
                        log_file = "log_ga_" + dataset_size + "_" + self.mutacao_entry.get() + "_" + self.populacao_entry.get() + "_" + self.iteracoes_entry.get()
                    case "nn":
                        log_file = "log_nn_" + dataset_size

            self.atualizar_barra_progresso(log_file, iteracoes_selecionadas)
            stdout, stderr = process.communicate()

            # Calcula o tempo de execução após a execução do processo
            self.tempo_execucao = time.time() - start_time

            print(f"Tempo de execução do algoritmo em C: {self.tempo_execucao} segundos")

            print(stdout)
            print(stderr)

            numeros_strings = stdout[1:-1].split(', ')
            caminho_resutado = [int(num) for num in numeros_strings]

            # Atualizar o caminho com o resultado do algoritmo
            self.caminho = caminho_resutado
            print("Caminho válido: " + str(self.valida_caminho()))

            # Atualizar o gráfico na interface
            self.update_graph()
            self.run_button.configure(state="normal")

            # if(algoritmo_sigla != "nn"):
            #     self.analisar_log_e_gerar_graficos(log_file, iteracoes_selecionadas, self.get_distancia_otima())

        # Cria e inicia a thread para executar o algoritmo
        thread = threading.Thread(target=run)
        thread.start()
    
    def calcula_distancia_caminho(self):
        distancia_caminho = 0.0
        tam = len(self.caminho)
        
        match tam:
            case 101:
                coordenadas = self.open_dataset(os.path.join("datasets","star100.xyz.txt"))
            case 1001:
                coordenadas = self.open_dataset(os.path.join("datasets","star1k.xyz.txt"))
            case 10001:
                coordenadas = self.open_dataset(os.path.join("datasets","star10k.xyz.txt"))
            case 37860:
                coordenadas = self.open_dataset(os.path.join("datasets","kj37859.xyz.txt")) 
            case 109400:
                coordenadas = self.open_dataset(os.path.join("datasets","hyg109399.xyz.txt"))
        
        for i in range(tam - 1):
            x1, y1, z1 = coordenadas[self.caminho[i]][1], coordenadas[self.caminho[i]][2], coordenadas[self.caminho[i]][3]
            x2, y2, z2 = coordenadas[self.caminho[i+1]][1], coordenadas[self.caminho[i+1]][2], coordenadas[self.caminho[i+1]][3]
            distancia = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            distancia_caminho += distancia
    
        return distancia_caminho

    def quit_app(self):
        self.root.quit()
        self.root.destroy()

    def plota_caminho(self, caminho):
        tam = len(caminho)
        self.ax.set_facecolor("#000000")
        self.ax.tick_params(axis='x', colors='#E0E0E0')
        self.ax.tick_params(axis='y', colors='#E0E0E0')
        self.ax.tick_params(axis='z', colors='#E0E0E0')
        self.ax.yaxis.label.set_color('#E0E0E0')
        self.ax.xaxis.label.set_color('#E0E0E0')
        self.ax.zaxis.label.set_color('#E0E0E0')
        self.ax.grid(False)

        coordenadas_x = np.arange(tam, dtype=float)
        coordenadas_y = np.arange(tam, dtype=float)
        coordenadas_z = np.arange(tam, dtype=float)

        grossura_linha = 2;

        match tam:
            case 101:
                coordenadas = self.open_dataset(os.path.join("datasets", "star100.xyz.txt"))
                grossura_linha = 1;
            case 1001:
                coordenadas = self.open_dataset(os.path.join("datasets", "star1k.xyz.txt"))
                grossura_linha = 1;
            case 10001:
                coordenadas = self.open_dataset(os.path.join("datasets", "star10k.xyz.txt"))
                grossura_linha = 0.5;
            case 37860:
                coordenadas = self.open_dataset(os.path.join("datasets", "kj37859.xyz.txt"))
                grossura_linha = 0.1;
            case 109400:
                coordenadas = self.open_dataset(os.path.join("datasets", "hyg109399.xyz.txt"))
                grossura_linha = 0.1;

        for i in range(tam):
            coordenadas_x[i] = coordenadas[caminho[i]][1]
            coordenadas_y[i] = coordenadas[caminho[i]][2]
            coordenadas_z[i] = coordenadas[caminho[i]][3]

        # Criar gradiente de cores do vermelho ao lilás (não cíclico)
        colormap = cm.hsv
        scaled_indices = np.linspace(0, 0.85, tam)  # Mapeia o gradiente de 0 (vermelho) a 0.83 (violeta)
        colors = colormap(scaled_indices)  # Aplica o colormap ao intervalo ajustado


        # Scatter plot com gradiente de cores
        if tam < 10000:
            self.ax.scatter(
                coordenadas_x[1:tam - 1],
                coordenadas_y[1:tam - 1],
                coordenadas_z[1:tam - 1],
                c=colors[1:tam - 1],
                s=8
            )

        # Criar segmentos de linha para aplicar o gradiente
        segments = [
            [[coordenadas_x[i], coordenadas_y[i], coordenadas_z[i]],
            [coordenadas_x[i + 1], coordenadas_y[i + 1], coordenadas_z[i + 1]]]
            for i in range(tam - 1)
        ]

        # Adicionar os segmentos com o gradiente de cores
        linha = Line3DCollection(segments, colors=colors[:-1], linewidth=grossura_linha)
        self.ax.add_collection3d(linha)

        # Destacar o ponto inicial (nó origem)
        self.ax.scatter(0, 0, 0, c='orange', s=15)

        RADIUS = max(coordenadas_x.max(), coordenadas_y.max(), coordenadas_z.max()) * 1.33
        self.ax.set_xlim3d(-RADIUS / 2, RADIUS / 2)
        self.ax.set_zlim3d(-RADIUS / 2, RADIUS / 2)
        self.ax.set_ylim3d(-RADIUS / 2, RADIUS / 2)

        return self.fig, self.ax
        
    def open_dataset(self, dataset_name):
        matriz = []
        with open(dataset_name, 'r') as arquivo:
            linhas = arquivo.readlines()
            for idx, linha in enumerate(linhas):
                valores = linha.split()
                if len(valores) == 3:
                    try:
                        x, y, z = map(float, valores)
                        matriz.append([idx, x, y, z])
                    except ValueError:
                        # Se a conversão para float falhar, tenta converter para int
                        x, y, z = map(int, valores)
                        matriz.append([idx, x, y, z])
        return np.array(matriz)
    
    def valida_caminho(self):

        # Verifica se o primeiro e o último elemento são 0
        if self.caminho[0] != 0 or self.caminho[-1] != 0:
            # Encontrar a posição do valor 0 no caminho
            pos_zero = self.caminho.index(0)

            # Ajustar o caminho para iniciar e terminar em 0, mantendo a ordem
            self.caminho = self.caminho[pos_zero:] + self.caminho[1:pos_zero] + [0]

        if self.caminho[0] != 0 or self.caminho[-1] != 0:
            return False
        
        # Cria um conjunto dos números esperados
        print(len(self.caminho))
        numeros_esperados = np.arange(len(self.caminho) - 1)
        numeros_esperados = np.insert(numeros_esperados, 0, 0)
        print(numeros_esperados)
        print()

        # Cria um conjunto dos números presentes no caminho, exceto o último 0
        numeros_no_caminho = np.sort(self.caminho)
        print(numeros_no_caminho)
        # Verifica se todos os números esperados estão presentes e se são únicos (exceto o último 0)
        return np.array_equal(numeros_no_caminho, numeros_esperados)


if __name__ == "__main__":
    root = ctk.CTk()
    app = AnimatedGraphApp(root)

    toolbar_frame = ctk.CTkFrame(app.frame_middle)
    toolbar_frame.pack(side=ctk.TOP, fill=ctk.X)
    toolbar = NavigationToolbar2Tk(app.canvas, toolbar_frame)
    toolbar.update()
    
    root.mainloop()