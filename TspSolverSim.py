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
        self.quit_button = ctk.CTkButton(self.frame_right, text="Quit", command=self.quit_app)
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

if __name__ == "__main__":
    root = ctk.CTk()
    app = AnimatedGraphApp(root)
    root.mainloop()
