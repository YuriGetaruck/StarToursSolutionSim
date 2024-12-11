import pandas as pd
import matplotlib.pyplot as plt

# Configurações gerais
optimal_distance = 1795
random_distance = 6971.13

# Função para carregar os dados
def load_data(filename, has_iterations=True):
    if has_iterations:
        return pd.read_csv(filename, header=None, names=["Iteration", "Total Distance", "Execution Time"])
    else:
        return pd.read_csv(filename, header=None, names=["Stars Visited", "Total Distance", "Execution Time"])

# Função para calcular métricas
def calculate_metrics(data, optimal_distance, random_distance):
    data["Improvement Rate"] = 1 - (data["Total Distance"] / data["Total Distance"].iloc[0])
    data["Convergence Rate"] = data["Improvement Rate"].diff().fillna(0)
    return data

# Função para gerar gráficos comparativos
def plot_comparative_graphs(data_dict, optimal_distance):
    plt.figure(figsize=(12, 8))

    # Gráfico: Taxa de melhoria x Tempo de execução
    # plt.subplot(3, 1, 1)
    for algorithm_name, data in data_dict.items():
        plt.plot(data["Execution Time"], data["Improvement Rate"], label=f"{algorithm_name} - Taxa de Melhoria")
    plt.title("Taxa de Melhoria x Tempo de Execução")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Taxa de Melhoria")
    plt.grid()
    plt.legend()

    plt.figure(figsize=(24, 5))

    # Gráfico: Taxa de convergência x Tempo de execução
    # plt.subplot(3, 1, 2)
    for algorithm_name, data in data_dict.items():
        plt.plot(data["Execution Time"], data["Convergence Rate"], label=f"{algorithm_name} - Taxa de Convergência")
    plt.title("Taxa de Convergência x Tempo de Execução")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Taxa de Convergência")
    plt.grid()
    plt.legend()

    plt.figure(figsize=(12, 8))

    # Gráfico: Distância total x Tempo de execução
    # plt.subplot(3, 1, 3)
    for algorithm_name, data in data_dict.items():
        plt.plot(data["Execution Time"], data["Total Distance"], label=f"{algorithm_name} - Distância Total")
    plt.axhline(y=optimal_distance, color='red', linestyle='--', label="Distância Ótima")
    plt.title("Distância Total x Tempo de Execução")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Distância Total")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig("comparative_graphs.png")
    plt.show()

# Processando os arquivos
aco_data = load_data("log_aco_100_100_2.60_3.00_0.40_10.00_50.txt")
ga_data = load_data("log_ga_100_0.15_250_7000.txt")
grasp_data = load_data("log_grasp_100_0.25_4000.txt")
# nn_data = load_data("log_nn_100.txt", has_iterations=False)

# Calculando métricas
aco_data = calculate_metrics(aco_data, optimal_distance, random_distance)
ga_data = calculate_metrics(ga_data, optimal_distance, random_distance)
grasp_data = calculate_metrics(grasp_data, optimal_distance, random_distance)
# nn_data = calculate_metrics(nn_data, optimal_distance, random_distance)

# Criando dicionário de dados
data_dict = {
    "ACO": aco_data,
    "GA": ga_data,
    "GRASP": grasp_data
    # "NN": nn_data
}

# Gerando gráficos comparativos
plot_comparative_graphs(data_dict, optimal_distance)
