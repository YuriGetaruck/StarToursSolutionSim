import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np

class AnimatedGraphApp:
    def __init__(self, root):
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
        
        self.freq_label = ctk.CTkLabel(self.frame_right, text="Frequência:")
        self.freq_label.pack(pady=5)
        self.freq_var = ctk.DoubleVar(value=1.0)
        self.freq_scale = ctk.CTkSlider(self.frame_right, from_=0.1, to=5.0, number_of_steps=49, variable=self.freq_var)
        self.freq_scale.pack(pady=5)
        
        self.amp_label = ctk.CTkLabel(self.frame_right, text="Amplitude:")
        self.amp_label.pack(pady=5)
        self.amp_var = ctk.DoubleVar(value=1.0)
        self.amp_scale = ctk.CTkSlider(self.frame_right, from_=0.1, to=5.0, number_of_steps=49, variable=self.amp_var)
        self.amp_scale.pack(pady=5)
        
        # Botão Quit
        self.quit_button = ctk.CTkButton(self.frame_right, text="FECHAR", command=self.quit_app)
        self.quit_button.pack(pady=20)
        
        # Configuração do gráfico 3D
        self.fig = plt.figure(facecolor="#2E2E2E")
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor="#2E2E2E")
        self.ax.set_facecolor("#2E2E2E")
        self.ax.tick_params(axis='x', colors='#E0E0E0')
        self.ax.tick_params(axis='y', colors='#E0E0E0')
        self.ax.tick_params(axis='z', colors='#E0E0E0')
        self.ax.yaxis.label.set_color('#E0E0E0')
        self.ax.xaxis.label.set_color('#E0E0E0')
        self.ax.zaxis.label.set_color('#E0E0E0')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_left)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
        
        self.x = np.linspace(-5, 5, 100)
        self.y = np.linspace(-5, 5, 100)
        self.x, self.y = np.meshgrid(self.x, self.y)
        self.z = np.sin(np.sqrt(self.x**2 + self.y**2))
        self.surf = self.ax.plot_surface(self.x, self.y, self.z, color="#800080")  # Superfície roxa
        
        self.ani = animation.FuncAnimation(self.fig, self.update_graph, interval=100)

        # Configurar o protocolo de fechamento de janela
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
    def update_graph(self, frame):
        self.ax.clear()
        freq = self.freq_var.get()
        amp = self.amp_var.get()
        self.z = amp * np.sin(np.sqrt(self.x**2 + self.y**2) + frame * 0.1 * freq)
        self.surf = self.ax.plot_surface(self.x, self.y, self.z, color="#800080")
        self.ax.set_facecolor("#2E2E2E")
        self.ax.tick_params(axis='x', colors='#E0E0E0')
        self.ax.tick_params(axis='y', colors='#E0E0E0')
        self.ax.tick_params(axis='z', colors='#E0E0E0')
        self.ax.yaxis.label.set_color('#E0E0E0')
        self.ax.xaxis.label.set_color('#E0E0E0')
        self.ax.zaxis.label.set_color('#E0E0E0')
        self.canvas.draw()

    def quit_app(self):
        self.root.quit()
        self.root.destroy()

# if __name__ == "__main__":
#     root = ctk.CTk()
#     app = AnimatedGraphApp(root)
#     root.mainloop()



# fucao que recebe um vetor com os IDs da ordem do caminho gerado e plota esse caminho em 3D
def plota_caminho(caminho):
    tam = len(caminho)
    ax = plt.figure().add_subplot(projection='3d')


    coordenadas_plot = np.arange(((tam) * 3), dtype=float)
    coordenadas_plot = coordenadas_plot.reshape(tam, 3)

    coordenadas_x = np.arange(tam, dtype=float)
    coordenadas_y = np.arange(tam, dtype=float)
    coordenadas_z = np.arange(tam, dtype=float)

    match tam:
        case 101:
            coordenadas = open_dataset("datasets\\star100.xyz.txt")
        case 10001:
            coordenadas = open_dataset("datasets\\star1k.xyz.txt")
        case 37860:
            coordenadas = open_dataset("datasets\\kj37859.xyz.txt")  
        case 109400:
            coordenadas = open_dataset("datasets\\hyg109399.xyz.txt")   
    
    for i in range(tam):
        coordenadas_x[i] = coordenadas[caminho[i]][1]
        coordenadas_y[i] = coordenadas[caminho[i]][2]
        coordenadas_z[i] = coordenadas[caminho[i]][3]

    ax.scatter(coordenadas_x[1:tam - 1], coordenadas_y[1:tam - 1],
               coordenadas_z[1:tam - 1], c='blue', s=15)

    ax.plot(coordenadas_x, coordenadas_y, coordenadas_z, color='k')

    ax.scatter(0, 0, 0, c='orange', s=80)

    plt.show()

#############################################################################################################################################

def open_dataset(dataset_neme):
    matriz = []
    with open(dataset_neme, 'r') as arquivo:
        linhas = arquivo.readlines()
        for idx, linha in enumerate(linhas):
            valores = linha.split()
            if len(valores) == 3:
                x, y, z = map(float, valores)
                matriz.append([idx, x, y, z])
    return np.array(matriz)

caminho = [0, 3, 1, 2, 4, 7, 23, 41, 16, 9, 28, 40, 38, 35, 66, 75, 91, 86, 46, 64, 44, 77, 82, 69, 63, 55, 45, 31, 27, 20, 59, 74, 76, 68, 56, 12, 11, 24, 17, 43, 84, 70, 52, 51, 81, 60, 78, 39, 37, 5, 10, 34, 48, 50, 85, 79, 80, 65, 62, 36, 25, 29, 67, 89, 33, 53, 49, 94, 92, 88, 15, 21, 26, 6, 22, 8, 19, 18, 30, 99, 95, 98, 42, 54, 57, 72, 61, 73, 87, 97, 13, 14, 32, 58, 93, 83, 71, 96, 90, 47, 0]

print(len(caminho))
plota_caminho(caminho)