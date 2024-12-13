import pandas as pd
import matplotlib.pyplot as plt

# Configurações gerais
optimal_distance = 28235453
random_distance = 956099988.75
nn_distance = 32770020.00
nn_time = 66.028

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
    for algorithm_name, data in data_dict.items():
        plt.plot(data["Execution Time"], data["Improvement Rate"], label=f"{algorithm_name} - Taxa de Melhoria")
    plt.title("Taxa de Melhoria x Tempo de Execução")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Taxa de Melhoria")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig("Taxa de melhoria x Tempo de execução.png")
    plt.show()

    plt.figure(figsize=(24, 5))

    # Gráfico: Taxa de convergência x Tempo de execução
    for algorithm_name, data in data_dict.items():
        plt.plot(data["Execution Time"], data["Convergence Rate"], label=f"{algorithm_name} - Taxa de Convergência")
    plt.title("Taxa de Convergência x Tempo de Execução")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Taxa de Convergência")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig("Taxa de convergência x Tempo de execução.png")
    plt.show()

    plt.figure(figsize=(12, 8))

    # Gráfico: Distância total x Tempo de execução
    for algorithm_name, data in data_dict.items():
        plt.plot(data["Execution Time"], data["Total Distance"], label=f"{algorithm_name} - Distância Total")
    plt.axhline(y=optimal_distance, color='red', linestyle='--', label="Distância Ótima")
    plt.title("Distância Total x Tempo de Execução")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Distância Total")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig("Distância total x Tempo de execução.png")
    plt.show()

# Função para gerar gráfico de barras comparativo
def plot_bar_comparison(data_dict, optimal_distance, random_distance):
    best_results = {
        algorithm_name: data["Total Distance"].min()
        for algorithm_name, data in data_dict.items()
    }

    algorithms = list(best_results.keys())
    best_distances = list(best_results.values())
    optimal_distances = [optimal_distance] * len(algorithms)
    random_distances = [random_distance] * len(algorithms)
    nn_distances = [nn_distance] * len(algorithms)

    # Gráfico de barras
    x = range(len(algorithms))
    width = 0.25

    plt.figure(figsize=(10, 6))
    plt.bar(x, best_distances, width=width, label="Melhor Resultado", color="blue")
    plt.bar([p + width for p in x], optimal_distances, width=width, label="Distância Ótima", color="green")
    plt.bar([p + 2 * width for p in x], nn_distances, width=width, label="Distância NN", color="purple")
    plt.bar([p + 3 * width for p in x], random_distances, width=width, label="Distância Aleatória", color="red")

    plt.xlabel("Algoritmos")
    plt.ylabel("Distância")
    plt.title("Comparação de Distâncias Obtidas")
    plt.xticks([p + width for p in x], algorithms)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig("bar_comparison.png")
    plt.show()

# Função para gerar gráfico de barras do tempo até o melhor caminho
def plot_time_to_best_path(data_dict):
    best_times = {
        algorithm_name: data.loc[data["Total Distance"].idxmin(), "Execution Time"]
        for algorithm_name, data in data_dict.items()
    }

    algorithms = list(best_times.keys())
    algorithms.append("NN")
    times = list(best_times.values())
    times.append(nn_time)

    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, times, color="gray", alpha=0.8)
    plt.xlabel("Algoritmos")
    plt.ylabel("Tempo (s)")
    plt.title("Tempo até o Melhor Caminho Encontrado")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig("tempo_ate_melhor_caminho.png")
    plt.show()

# Processando os arquivos
aco_data = load_data("log_aco_37859_100_2.60_3.00_0.40_10.00_50.txt")
ga_data = load_data("log_ga_37859_0.15_250_100000.txt")
grasp_data = load_data("log_grasp_37859_0.25_4000.txt")
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
plot_bar_comparison(data_dict, optimal_distance, random_distance)
plot_time_to_best_path(data_dict)

