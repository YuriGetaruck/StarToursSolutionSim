import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
import subprocess
import threading
import os
import platform
import time
import re

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
        self.root.geometry("1600x990") #ratio 400:217

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
        self.mutacao_slider = ctk.CTkSlider(self.frame_left, from_=0.00, to=1.00, number_of_steps=100, command=self.update_mutacao)
        self.mutacao_slider.pack(pady=5)
        self.mutacao_var = ctk.StringVar(value="0.08")
        self.mutacao_entry = ctk.CTkEntry(self.frame_left, textvariable=self.mutacao_var)
        self.mutacao_entry.pack(pady=5)

        self.populacao_label = ctk.CTkLabel(self.frame_left, text="Tamanho da População:")
        self.populacao_label.pack(pady=5)
        self.populacao_entry = ctk.CTkEntry(self.frame_left)
        self.populacao_entry.pack(pady=5)

        self.iteracoes_label = ctk.CTkLabel(self.frame_left, text="Número de Iterações:")
        self.iteracoes_label.pack(pady=5)
        self.iteracoes_entry = ctk.CTkEntry(self.frame_left)
        self.iteracoes_entry.pack(pady=5)

        # Hiperparâmetros para Algoritmo de Colônia de Formigas (ACO)
        self.n_ants_label = ctk.CTkLabel(self.frame_left, text="Número de Formigas:")
        self.n_ants_label.pack(pady=5)
        self.n_ants_var = ctk.StringVar(value="50")  # Cria um StringVar com o valor padrão
        self.n_ants_entry = ctk.CTkEntry(self.frame_left, textvariable=self.n_ants_var)
        self.n_ants_entry.pack(pady=5)

        self.n_iterations_label = ctk.CTkLabel(self.frame_left, text="Número de Iterações:")
        self.n_iterations_label.pack(pady=5)
        self.n_iterations_var = ctk.StringVar(value="200")  # Cria um StringVar com o valor padrão
        self.n_iterations_entry = ctk.CTkEntry(self.frame_left, textvariable=self.n_iterations_var)
        self.n_iterations_entry.pack(pady=5)

        self.alpha_label = ctk.CTkLabel(self.frame_left, text="Valor de Alpha:")
        self.alpha_label.pack(pady=5)
        self.alpha_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=1.0, number_of_steps=100, command=self.update_alpha)
        self.alpha_slider.pack(pady=5)
        self.alpha_var = ctk.StringVar(value="1.00")
        self.alpha_entry = ctk.CTkEntry(self.frame_left, textvariable=self.alpha_var)
        self.alpha_entry.pack(pady=5)

        self.beta_label = ctk.CTkLabel(self.frame_left, text="Valor de Beta:")
        self.beta_label.pack(pady=5)
        self.beta_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=1.0, number_of_steps=100, command=self.update_beta)
        self.beta_slider.pack(pady=5)
        self.beta_var = ctk.StringVar(value="1.00")
        self.beta_entry = ctk.CTkEntry(self.frame_left, textvariable=self.beta_var)
        self.beta_entry.pack(pady=5)

        self.evaporation_label = ctk.CTkLabel(self.frame_left, text="Taxa de Evaporação:")
        self.evaporation_label.pack(pady=5)
        self.evaporation_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=1.0, number_of_steps=100, command=self.update_evaporation)
        self.evaporation_slider.pack(pady=5)
        self.evaporation_var = ctk.StringVar(value="0.3")
        self.evaporation_entry = ctk.CTkEntry(self.frame_left, textvariable=self.evaporation_var)
        self.evaporation_entry.pack(pady=5)

        self.q_label = ctk.CTkLabel(self.frame_left, text="Valor de Q:")
        self.q_label.pack(pady=5)
        self.q_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=1.0, number_of_steps=100, command=self.update_q)
        self.q_slider.pack(pady=5)
        self.q_var = ctk.StringVar(value="0.3")
        self.q_entry = ctk.CTkEntry(self.frame_left, textvariable=self.q_var)
        self.q_entry.pack(pady=5)

        # Hiperparâmetros para GRASP
        self.grasp_alpha_label = ctk.CTkLabel(self.frame_left, text="Alpha:")
        self.grasp_alpha_label.pack(pady=5)
        self.grasp_alpha_slider = ctk.CTkSlider(self.frame_left, from_=0.0, to=1.0, number_of_steps=100, command=self.update_grasp_alpha)
        self.grasp_alpha_slider.pack(pady=5)
        self.grasp_alpha_var = ctk.StringVar(value="0.10")
        self.grasp_alpha_entry = ctk.CTkEntry(self.frame_left, textvariable=self.grasp_alpha_var)
        self.grasp_alpha_entry.pack(pady=5)

        self.grasp_iterations_label = ctk.CTkLabel(self.frame_left, text="Número de Iterações:")
        self.grasp_iterations_label.pack(pady=5)
        self.grasp_iterations_var = ctk.StringVar(value="1000")  # Cria um StringVar com o valor padrão
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
        
        # self.caminho_label = ctk.CTkLabel(self.frame_right, text="Caminho:")
        # self.caminho_label.pack(pady=5)
        # self.caminho_text = ctk.CTkTextbox(self.frame_right, height=300, width=400)
        # self.caminho_text.pack(pady=5)
        # self.caminho_text.insert(ctk.END, self.caminho)
        
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

        # Elementos da interface
        self.progress_label = ctk.CTkLabel(self.frame_right, text="Progresso do Algoritmo: ", font=("Arial", 16))
        self.progress_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.frame_right, width=300)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

        self.progress_percentage = ctk.CTkLabel(self.frame_right, text="0%", font=("Arial", 14))
        self.progress_percentage.pack(pady=10)
        
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
            
            match self.dataset_select.get():
                case "100 Estrelas":
                    dataset_tour = "star100_tour.txt"
                    dataset_name = "star100.xyz.txt"
                case "1.000 Estrelas":
                    dataset_tour = "star1k_tour.txt"
                    dataset_name = "star1k.xyz.txt"
                case "10.000 Estrelas":
                    dataset_tour = "star10k_tour.txt"
                    dataset_name = "star10k.xyz.txt"
                case "37.859 Estrelas":
                    dataset_tour = "kj37859_tour.txt"
                    dataset_name = "kj37859.xyz.txt"
                case "109.399 Estrelas":
                    dataset_tour = "hyg109399_tour.txt"
                    dataset_name = "hyg109399.xyz.txt"
        
            # Nome do arquivo do melhor caminho (alterar conforme necessário)
            best_path_file = "best_paths/" + dataset_tour
            
            # Carregar o melhor caminho do arquivo
            with open(best_path_file, 'r') as file:
                best_path = [int(line.strip()) for line in file]

            for i in range(len(best_path)):
                best_path[i] = best_path[i] - 1
            
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
            
            self.ax.plot(coordenadas_x, coordenadas_y, coordenadas_z, color='red', linewidth=1)

            # Atualizar o canvas com o novo gráfico
            self.canvas.draw()
        else:
            self.update_graph()

    def atualizar_barra_progresso(self, algoritmo, iteracoes_totais):
        def atualizar_barra_progresso_sub_process(algoritmo, iteracoes_totais):
            iteracao_atual = 0
            while iteracao_atual < int(iteracoes_totais):
                with open("c_scripts\\logs\\log_" + algoritmo, "r") as file:
                    linhas = file.readlines()
                
                # Extrair a última iteração do log
                for linha in reversed(linhas):
                    match = re.search(r"Iteracao: (\d+)", linha)
                    if match:
                        iteracao_atual = int(match.group(1))
                        break
                
                # Atualizar a barra de progresso
                progresso = iteracao_atual / int(iteracoes_totais)
                self.progress_bar.set(progresso)
                self.progress_percentage.configure(text=f"{int(progresso * 100)}%")
                
                time.sleep(0.1)

        threading.Thread(target=atualizar_barra_progresso_sub_process, args=(algoritmo, iteracoes_totais)).start()


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
                    args = [algoritmo, dataset_name, self.grasp_iterations_var.get(), self.grasp_alpha_var.get()]
                    iteracoes_selecionadas = self.grasp_iterations_var.get()

            print(f"algoritmo: {algoritmo} dataset: {dataset_name} dataset_size: {dataset_size}")

            # Inicia a contagem de tempo antes de chamar o processo
            start_time = time.time()

            # Executa o processo
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if(algoritmo_sigla != "nn"):
                self.atualizar_barra_progresso(algoritmo_sigla, iteracoes_selecionadas)
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
        self.ax.set_facecolor("#2E2E2E")
        self.ax.tick_params(axis='x', colors='#E0E0E0')
        self.ax.tick_params(axis='y', colors='#E0E0E0')
        self.ax.tick_params(axis='z', colors='#E0E0E0')
        self.ax.yaxis.label.set_color('#E0E0E0')
        self.ax.xaxis.label.set_color('#E0E0E0')
        self.ax.zaxis.label.set_color('#E0E0E0')
        self.ax.grid(False)

        coordenadas_plot = np.arange(((tam) * 3), dtype=float)
        coordenadas_plot = coordenadas_plot.reshape(tam, 3)

        coordenadas_x = np.arange(tam, dtype=float)
        coordenadas_y = np.arange(tam, dtype=float)
        coordenadas_z = np.arange(tam, dtype=float)

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

        for i in range(tam):
            coordenadas_x[i] = coordenadas[caminho[i]][1]
            coordenadas_y[i] = coordenadas[caminho[i]][2]
            coordenadas_z[i] = coordenadas[caminho[i]][3]

        self.ax.scatter(coordenadas_x[1:tam - 1], coordenadas_y[1:tam - 1],
                    coordenadas_z[1:tam - 1], c='red', s=0.1)

        self.ax.plot(coordenadas_x, coordenadas_y, coordenadas_z, color='yellow', linewidth=1)

        self.ax.scatter(0, 0, 0, c='orange', s=15)
        return self.fig, self.ax
    
    def open_dataset(self, dataset_neme):
        matriz = []
        with open(dataset_neme, 'r') as arquivo:
            linhas = arquivo.readlines()
            for idx, linha in enumerate(linhas):
                valores = linha.split()
                if len(valores) == 3:
                    x, y, z = map(float, valores)
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
        
        # Cria um conjunto dos números presentes no caminho, exceto o último 0
        numeros_no_caminho = np.sort(self.caminho)
        
        # Verifica se todos os números esperados estão presentes e se são únicos (exceto o último 0)
        if numeros_no_caminho.all() == numeros_esperados.all():
            return True
        else:
            return False

if __name__ == "__main__":
    root = ctk.CTk()
    app = AnimatedGraphApp(root)

    toolbar_frame = ctk.CTkFrame(app.frame_middle)
    toolbar_frame.pack(side=ctk.TOP, fill=ctk.X)
    toolbar = NavigationToolbar2Tk(app.canvas, toolbar_frame)
    toolbar.update()
    
    root.mainloop()