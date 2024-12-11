import subprocess
import os
import csv
import itertools
import numpy as np

# Função para ler o valor do log CSV
def read_log_value(dataset_size, n_ants, alpha, beta, evaporation, q, n_iterations):
    log_filename = f"c_scripts\\logs\\log_aco_{dataset_size}_{n_ants}_{alpha:.2f}_{beta:.2f}_{evaporation:.2f}_{q:.2f}_{n_iterations}.txt"
    
    if not os.path.exists(log_filename):
        print(f"Log file {log_filename} not found.")
        return None
    
    # Lê a última linha e retorna o valor a ser minimizado (segunda coluna)
    with open(log_filename, 'r') as file:
        reader = csv.reader(file)
        last_row = list(reader)[-1]
        return float(last_row[1])

# Função para chamar o algoritmo ACO em C
def run_aco(dataset_size, n_ants, alpha, beta, evaporation, q, n_iterations):
    args = [
        "c_scripts\\aco.exe", "star100.xyz.txt", 
        str(dataset_size), str(n_ants), str(n_iterations), 
        f"{alpha:.2f}", f"{beta:.2f}", f"{evaporation:.2f}", str(q)
    ]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout

# Função para realizar o grid search
def grid_search(dataset_sizes, n_ants_list, alphas, betas, evaporations, q_list, iterations_list):
    best_value = float('inf')
    best_params = None
    
    # Certifique-se de que as pastas "grids" e "logs" existem
    os.makedirs("grids", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Nome dos arquivos de log
    grid_log_file = "grids\\log_grid_aco.csv"
    text_log_file = "logs\\log_grid_aco.txt"
    
    # Abre os arquivos de log
    with open(grid_log_file, 'w', newline='') as csv_file, open(text_log_file, 'w') as txt_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Dataset Size", "Number of Ants", "Alpha", "Beta", "Evaporation", "Q", "Iterations", "Result"])
        
        # Gerando todas as combinações possíveis de hiperparâmetros
        for dataset_size, n_ants, alpha, beta, evaporation, q, n_iterations in itertools.product(
            dataset_sizes, n_ants_list, alphas, betas, evaporations, q_list, iterations_list
        ):
            log_message = (
                f"Running ACO with dataset_size={dataset_size}, n_ants={n_ants}, "
                f"alpha={alpha:.2f}, beta={beta:.2f}, evaporation={evaporation:.2f}, "
                f"q={q}, iterations={n_iterations}"
            )
            print(log_message)  # Exibe no terminal
            txt_file.write(log_message + '\n')  # Salva no arquivo de texto
            
            # Chama o algoritmo ACO
            run_aco(dataset_size, n_ants, alpha, beta, evaporation, q, n_iterations)
            
            # Lê o valor do log
            log_value = read_log_value(dataset_size, n_ants, alpha, beta, evaporation, q, n_iterations)
            
            # Escreve os resultados no CSV
            csv_writer.writerow([dataset_size, n_ants, f"{alpha:.2f}", f"{beta:.2f}", f"{evaporation:.2f}", q, n_iterations, log_value])
            
            # Atualiza os melhores parâmetros
            if log_value is not None and log_value < best_value:
                best_value = log_value
                best_params = (dataset_size, n_ants, alpha, beta, evaporation, q, n_iterations)
        
        # Escreve o melhor resultado no final do CSV
        csv_writer.writerow([])
        csv_writer.writerow(["Best Result"])
        csv_writer.writerow(["Dataset Size", "Number of Ants", "Alpha", "Beta", "Evaporation", "Q", "Iterations", "Result"])
        csv_writer.writerow([best_params[0], best_params[1], f"{best_params[2]:.2f}", f"{best_params[3]:.2f}", f"{best_params[4]:.2f}", best_params[5], best_params[6], best_value])
        
        # Também registra o melhor resultado no log de texto
        best_message = (
            f"Best result: {best_value} with parameters: dataset_size={best_params[0]}, "
            f"n_ants={best_params[1]}, alpha={best_params[2]:.2f}, beta={best_params[3]:.2f}, "
            f"evaporation={best_params[4]:.2f}, q={best_params[5]}, iterations={best_params[6]}"
        )
        print(best_message)  # Exibe no terminal
        txt_file.write(best_message + '\n')  # Salva no arquivo de texto
    
    return best_params, best_value

# Definição dos intervalos e step sizes para os hiperparâmetros
dataset_sizes = [100]  # Apenas um valor fixo, 100
n_ants_list = np.arange(50, 151, 50)  # Número de formigas: de 10 a 100 com passo 10
alphas = np.arange(0.1, 3.1, 0.5)  # Alpha: de 0.1 a 2.0 com passo 0.1
betas = np.arange(1.0, 5.1, 1)  # Beta: de 1.0 a 5.0 com passo 0.5
evaporations = np.arange(0.1, 1.1, 0.3)  # Evaporação: de 0.1 a 1.0 com passo 0.1
q_list = np.arange(0, 16, 5)  # Q: valores discretos
iterations_list = [200]  # Iterações: de 1000 a 5000 com passo 1000

# Realizando o grid search
best_params, best_value = grid_search(dataset_sizes, n_ants_list, alphas, betas, evaporations, q_list, iterations_list)
