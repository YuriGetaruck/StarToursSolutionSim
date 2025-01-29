import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurações gerais
optimal_distance = 276750
random_distance = 5221714.00
nn_distance = 310362.97
nn_time = 4.658

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

# Função para gerar gráficos comparativos ajustados com rótulos para as linhas de referência
def plot_comparative_graphs(data_dict, optimal_distance):
    plt.figure(figsize=(12, 8))

    # Gráfico: Taxa de melhoria x Tempo de execução
    for algorithm_name, data in data_dict.items():
        plt.plot(
            data["Execution Time"], 
            data["Improvement Rate"], 
            label=f"{algorithm_name} - Taxa de Melhoria"
        )
    plt.title("Taxa de Melhoria x Tempo de Execução", fontsize=14)
    plt.xlabel("Tempo de Execução (s)", fontsize=12)
    plt.ylabel("Taxa de Melhoria", fontsize=12)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig("Taxa_de_melhoria_x_Tempo_de_execucao.png")
    plt.show()

    plt.figure(figsize=(12, 5))

    # Gráfico: Taxa de convergência x Tempo de execução
    for algorithm_name, data in data_dict.items():
        plt.plot(data["Execution Time"], data["Convergence Rate"], label=f"{algorithm_name} - Taxa de Convergência", linewidth=1, alpha=1)

    # plt.yscale('log')  # Ajusta o eixo Y para escala logarítmica
    plt.yscale('symlog', linthresh=0.0001)  # Escala SymLog com limiar linear em torno de 0.0001
    plt.title("Taxa de Convergência x Tempo de Execução")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Taxa de Convergência (escala log)")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig("Taxa de convergência x Tempo de execução.png")
    plt.show()

    plt.figure(figsize=(12, 8))

    # Gráfico: Distância total x Tempo de execução
    for algorithm_name, data in data_dict.items():
        plt.plot(
            data["Execution Time"], 
            data["Total Distance"], 
            label=f"{algorithm_name} - Distância Total",
            linestyle='-'
        )
    # Adicionando linhas horizontais para valores de referência
    plt.axhline(y=optimal_distance, color='red', linestyle='--', label="Distância Ótima - " + f"{optimal_distance:.2f}")

    plt.axhline(y=nn_distance, color='purple', linestyle='--', label="Distância NN - " + f"{nn_distance:.2f}")

    plt.title("Distância Total x Tempo de Execução", fontsize=14)
    plt.xlabel("Tempo de Execução (s)", fontsize=12)
    plt.ylabel("Distância Total", fontsize=12)
    plt.grid(visible=True, which='both', linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.yscale('log', base = 10)
    plt.savefig("Distancia_total_x_Tempo_de_execucao.png")
    plt.show()

def plot_bar_comparison(data_dict):
    # Determina os melhores resultados para cada algoritmo
    best_results = {
        "GA": float(data_dict["GA"]["Total Distance"].min() if isinstance(data_dict["GA"], pd.DataFrame) else data_dict["GA"].min()),
        "ACO": float(data_dict["ACO"]["Total Distance"].min() if isinstance(data_dict["ACO"], pd.DataFrame) else data_dict["ACO"].min()),
        "GRASP": float(data_dict["GRASP"]["Total Distance"].min() if isinstance(data_dict["GRASP"], pd.DataFrame) else data_dict["GRASP"].min()),
        "NN": float(nn_distance),
        "ÓTIMO": float(optimal_distance),
    }

    # Ordena os algoritmos do maior para o menor resultado
    sorted_algorithms = sorted(best_results.items(), key=lambda x: x[1], reverse=True)

    # Separa os nomes e os valores em listas
    algorithms, best_distances = zip(*sorted_algorithms)

    # Definição de cores para cada algoritmo
    colors = ["purple", "orange", "blue", "green", "red"]

    # Gera o gráfico
    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        np.arange(len(algorithms)), best_distances, color=colors, alpha=0.9, edgecolor="black"
    )

    # Adiciona rótulos nas barras
    for bar, distance in zip(bars, best_distances):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{distance:.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    # Configurações do gráfico
    plt.xlabel("Algoritmos")
    plt.ylabel("Melhor Distância")
    plt.title("Comparativo de Desempenho dos Algoritmos")
    plt.xticks(np.arange(len(algorithms)), algorithms)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Exibe o gráfico
    plt.tight_layout()
    plt.savefig("bar_comparison.png")
    plt.show()

# Processando os arquivos
aco_data = load_data("log_aco_10000_100_1.60_2.00_0.70_15.00_20000.txt")
ga_data = load_data("log_ga_10000_0.15_250_100000.txt")
grasp_data = load_data("log_grasp_10000_0.25_1000000.txt")
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
plot_bar_comparison(data_dict)

