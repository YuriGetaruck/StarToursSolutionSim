import pandas as pd
import matplotlib.pyplot as plt
import os

# Nome dos arquivos e valores ótimos
files = {
    "log_nn_100.txt": 1795,
    "log_nn_1000.txt": 22227,
    "log_nn_10000.txt": 276750,
    "log_nn_37859.txt": 28235453,
    "log_nn_109399.txt": 13750874,
}

# Dicionário para armazenar os dataframes
dataframes = {}
proximidades_finais = {}

# Lê os arquivos e armazena em dataframes
for file, optimal in files.items():
    if os.path.exists(file):
        df = pd.read_csv(file, header=None, names=["Caminho", "Distancia", "Tempo"])
        df["Ótimo"] = optimal
        dataframes[file] = df
        # Calcula a proximidade para a última linha
        ultima_distancia = df.iloc[-1]["Distancia"]
        proximidades_finais[file] = ( optimal / ultima_distancia) * 100
    else:
        print(f"Arquivo {file} não encontrado.")

# Gráfico 1: Comparação entre tamanho do caminho e o tempo para os 5 CSVs
plt.figure(figsize=(10, 6))
for file, df in dataframes.items():
    plt.plot(df["Caminho"], df["Tempo"], label=file)
plt.xlabel("Tamanho do Caminho")
plt.ylabel("Tempo de Execução (s)")
plt.title("Comparação entre Tamanho do Caminho e Tempo de Execução")
plt.legend()
plt.grid()
plt.show()

# Gráfico 2: Comparação entre tempo de execução em barras para cada dataset
plt.figure(figsize=(10, 6))
datasets = list(files.keys())
tempos_totais = [df["Tempo"].sum() for df in dataframes.values()]
plt.bar(datasets, tempos_totais, color="gray")
plt.xlabel("Dataset")
plt.ylabel("Tempo Total de Execução (s)")
plt.title("Tempo de Execução por Dataset")
plt.grid(axis="y")
plt.show()

# Gráfico 3: Comparação da proximidade do ótimo
plt.figure(figsize=(10, 6))
plt.bar(proximidades_finais.keys(), proximidades_finais.values(), color="gray")
plt.xlabel("Dataset")
plt.ylabel("Proximidade do Ótimo (%)")
plt.title("Proximidade do Ótimo por Dataset")
plt.ylim(0, 100)  # Ajusta o eixo y para ir de 0 a 100
plt.grid(axis="y")
plt.show()

# Gráfico 4: Comparação entre o tamanho do caminho e a distância atual
plt.figure(figsize=(10, 6))
for file, df in dataframes.items():
    plt.plot(df["Caminho"], df["Distancia"], label=file)
plt.xlabel("Tamanho do Caminho")
plt.ylabel("Distância Atual")
plt.title("Comparação entre Tamanho do Caminho e Distância Atual")
plt.legend()
plt.grid()
plt.show()
