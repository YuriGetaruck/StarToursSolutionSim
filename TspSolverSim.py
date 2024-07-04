import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
import subprocess

class AnimatedGraphApp:
    def __init__(self, root):

        self.caminho = [0, 3, 1, 2, 4, 7, 23, 41, 16, 9, 28, 40, 38, 35, 66, 75, 91, 86, 46, 64, 44, 77, 82, 69, 63, 55, 45, 31, 27, 20, 59, 74, 76, 68, 56, 12, 11, 24, 17, 43, 84, 70, 52, 51, 81, 60, 78, 39, 37, 5, 10, 34, 48, 50, 85, 79, 80, 65, 62, 36, 25, 29, 67, 89, 33, 53, 49, 94, 92, 88, 15, 21, 26, 6, 22, 8, 19, 18, 
30, 99, 95, 98, 42, 54, 57, 72, 61, 73, 87, 97, 13, 14, 32, 58, 93, 83, 71, 96, 90, 47, 0]
        self.root = root
        self.root.title("Gráfico 3D Animado com Customização")
        ctk.set_appearance_mode("dark")  # Modo escuro
        ctk.set_default_color_theme("dark-blue")  # Tema azul escuro

        # Definir o tamanho da janela para Full HD
        self.root.geometry("1920x1080")

        # Configuração do layout
        self.frame_right = ctk.CTkFrame(self.root)
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.frame_left = ctk.CTkFrame(self.root)
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Parâmetros de customização
        self.param_label = ctk.CTkLabel(self.frame_right, text="Parâmetros de Customização")
        self.param_label.pack(pady=5)

        self.algoritmo_label = ctk.CTkLabel(self.frame_right, text="Algoritmo:")
        self.algoritmo_label.pack(pady=5)
        self.algoritmo_var = ctk.StringVar(value="Selecionar")
        self.algoritmo_select = ctk.CTkComboBox(self.frame_right, variable=self.algoritmo_var, values=["Nearest Neighbor (NN)", "Genetic Algorithm (GA)", "Ant Colony Optimization (ACO)"])
        self.algoritmo_select.pack(pady=5)

        self.dataset_label = ctk.CTkLabel(self.frame_right, text="Dataset:")
        self.dataset_label.pack(pady=5)
        self.dataset_var = ctk.StringVar(value="Selecionar")
        self.dataset_select = ctk.CTkComboBox(self.frame_right, variable=self.dataset_var, values=["100 Estrelas", "1.000 Estrelas", "10.000 Estrelas", "37.859 Estrelas", "109.399 Estrelas"])
        self.dataset_select.pack(pady=5)
        
        # Botao Run
        self.run_button = ctk.CTkButton(self.frame_right, text="RUN", command=self.run_algoritmo)
        self.run_button.pack(pady=20)

        # Botão Quit
        self.quit_button = ctk.CTkButton(self.frame_right, text="FECHAR", command=self.quit_app)
        self.quit_button.pack(pady=20)
        
        # Configuração do gráfico 3D
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.plota_caminho(self.caminho)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_left)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

        # Configurar o protocolo de fechamento de janela
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
    def update_graph(self):
        # Limpar o gráfico atual
        self.ax.clear()
        
        # Plotar o novo caminho
        self.plota_caminho(self.caminho)
        
        # Atualizar o canvas com o novo gráfico
        self.canvas.draw()

    def run_algoritmo(self):
        # Lógica para chamar o código em C aqui
        algoritmo = self.algoritmo_var.get()
        dataset = self.dataset_var.get()
        dataset_size = "100"
        dataset_name = "star100.xyz.txt"

        # Corrige nomes algoritmo e dataset
        match algoritmo:
            case "Nearest Neighbor (NN)":
                algoritmo = "c_scripts\\nn.exe"
            case "Genetic Algorithm (GA)":
                algoritmo = "c_scripts\\ga.exe"
            case "Ant Colony Optimization (ACO)":
                algoritmo = "c_scripts\\aco.exe"

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
        
        print("algoritmo: " + algoritmo + " dataset: " + dataset_name + " dataset_size: " + dataset_size)

        # Lógica para chamar o código em C e obter o caminho
        process = subprocess.Popen([algoritmo, dataset_name, dataset_size], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, 
                                    text=True)
        
        # Espera até que o processo termine
        stdout, stderr = process.communicate()

        print(stdout)
        print(stderr)
        
        numeros_strings = stdout[1:-1].split(', ')
        caminho_resutado = [int(num) for num in numeros_strings]

        # Atualizar o caminho com o resultado do algoritmo
        self.caminho = caminho_resutado
        
        # Atualizar o gráfico na interface
        self.update_graph()


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

        print(tam)

        match tam:
            case 101:
                coordenadas = self.open_dataset("datasets\\star100.xyz.txt")
            case 1001:
                coordenadas = self.open_dataset("datasets\\star1k.xyz.txt")
            case 10001:
                coordenadas = self.open_dataset("datasets\\star10k.xyz.txt")
            case 37860:
                coordenadas = self.open_dataset("datasets\\kj37859.xyz.txt")  
            case 109400:
                coordenadas = self.open_dataset("datasets\\hyg109399.xyz.txt")   

        for i in range(tam):
            coordenadas_x[i] = coordenadas[caminho[i]][1]
            coordenadas_y[i] = coordenadas[caminho[i]][2]
            coordenadas_z[i] = coordenadas[caminho[i]][3]

        self.ax.scatter(coordenadas_x[1:tam - 1], coordenadas_y[1:tam - 1],
                    coordenadas_z[1:tam - 1], c='blue', s=0.3)

        self.ax.plot(coordenadas_x, coordenadas_y, coordenadas_z, color='k', linewidth=0.2)

        self.ax.scatter(0, 0, 0, c='orange', s=30)
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

if __name__ == "__main__":
    root = ctk.CTk()
    app = AnimatedGraphApp(root)

    toolbar_frame = ctk.CTkFrame(app.frame_left)
    toolbar_frame.pack(side=ctk.TOP, fill=ctk.X)
    toolbar = NavigationToolbar2Tk(app.canvas, toolbar_frame)
    toolbar.update()
    
    root.mainloop()
