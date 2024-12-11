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
    data["Optimal Proximity"] = optimal_distance / data["Total Distance"]
    data["Better Than Random"] = random_distance / data["Total Distance"]
    data["Convergence Rate"] = data["Improvement Rate"].diff().fillna(0)
    return data

# Função para gerar gráficos
def plot_graphs(data, algorithm_name, optimal_distance, random_distance, is_iterative=True):
    plt.figure(figsize=(10, 6))
    
    if is_iterative:
        # Gráfico: Taxa de melhoria x Tempo de execução
        plt.plot(data["Execution Time"], data["Improvement Rate"], label="Taxa de Melhoria", color='blue')
        plt.title(f"Taxa de Melhoria x Tempo de Execução - {algorithm_name}")
        plt.xlabel("Tempo de Execução (s)")
        plt.ylabel("Taxa de Melhoria")
        plt.grid()
        plt.legend()
        plt.savefig(f"{algorithm_name}_taxa_de_melhoria.png")
        plt.show()
        
        # Gráfico: Taxa de convergência x Tempo de execução
        plt.plot(data["Execution Time"], data["Convergence Rate"], label="Taxa de Convergência", color='orange')
        plt.title(f"Taxa de Convergência x Tempo de Execução - {algorithm_name}")
        plt.xlabel("Tempo de Execução (s)")
        plt.ylabel("Taxa de Convergência")
        plt.grid()
        plt.legend()
        plt.savefig(f"{algorithm_name}_taxa_de_convergencia.png")
        plt.show()

    # Gráfico: Distância total x Tempo de execução
    plt.plot(data["Execution Time"], data["Total Distance"], label="Distância Total", color='green')
    plt.axhline(y=optimal_distance, color='red', linestyle='--', label="Distância Ótima")
    plt.title(f"Distância Total x Tempo de Execução - {algorithm_name}")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Distância Total")
    plt.grid()
    plt.legend()
    plt.savefig(f"{algorithm_name}_distancia_total.png")
    plt.show()

    # Gráfico: Proximidade do ótimo x Tempo de execução
    plt.plot(data["Execution Time"], data["Optimal Proximity"], label="Proximidade do Ótimo", color='purple')
    plt.title(f"Proximidade do Ótimo x Tempo de Execução - {algorithm_name}")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Proximidade do Ótimo")
    plt.grid()
    plt.legend()
    plt.savefig(f"{algorithm_name}_proximidade_do_otimo.png")
    plt.show()

    # Gráfico: Quão melhor que o aleatório x Tempo de execução
    plt.plot(data["Execution Time"], data["Better Than Random"], label="Melhor que Aleatório", color='brown')
    plt.title(f"Melhor que Aleatório x Tempo de Execução - {algorithm_name}")
    plt.xlabel("Tempo de Execução (s)")
    plt.ylabel("Melhor que Aleatório")
    plt.grid()
    plt.legend()
    plt.savefig(f"{algorithm_name}_melhor_que_aleatorio.png")
    plt.show()


# Processando os arquivos
aco_data = load_data("log_aco_100_100_2.60_3.00_0.40_10.00_50.txt")
ga_data = load_data("log_ga_100_0.15_250_7000.txt")
grasp_data = load_data("log_grasp_100_0.25_4000.txt")
nn_data = load_data("log_nn_100.txt", has_iterations=False)

# Calculando métricas
aco_data = calculate_metrics(aco_data, optimal_distance, random_distance)
ga_data = calculate_metrics(ga_data, optimal_distance, random_distance)
grasp_data = calculate_metrics(grasp_data, optimal_distance, random_distance)
nn_data = calculate_metrics(nn_data, optimal_distance, random_distance)

# Gerando gráficos para cada algoritmo
plot_graphs(aco_data, "ACO", optimal_distance, random_distance)
plot_graphs(ga_data, "GA", optimal_distance, random_distance)
plot_graphs(grasp_data, "GRASP", optimal_distance, random_distance)
plot_graphs(nn_data, "NN", optimal_distance, random_distance, is_iterative=False)
