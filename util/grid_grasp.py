import subprocess
import os
import csv
import itertools
import numpy as np

# Função para ler o valor do log CSV
def read_log_value(dataset_size, alpha, iterations):
    alpha_formatted = f"{alpha:.2f}"
    
    log_filename = f"c_scripts\\logs\\log_grasp_{dataset_size}_{alpha_formatted}_{iterations}.txt"
    
    if not os.path.exists(log_filename):
        print(f"Log file {log_filename} not found.")
        return None
    
    # Lê a última linha e retorna o valor a ser minimizado (segunda coluna)
    with open(log_filename, 'r') as file:
        reader = csv.reader(file)
        last_row = list(reader)[-1]
        return float(last_row[1])
    

# Função para chamar o algoritmo GRASP em C
def run_grasp(dataset_size, alpha, iterations):
    args = ["c_scripts\\grasp.exe", "star100.xyz.txt", str(iterations), str(alpha)]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout

# Função para realizar o grid search
def grid_search(dataset_sizes, alphas, iterations_list):
    best_value = float('inf')
    best_params = None
    
    # Certifique-se de que as pastas "grids" e "logs" existem
    os.makedirs("grids", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Nome dos arquivos de log
    grid_log_file = "grids\\log_grid_grasp.csv"
    text_log_file = "logs\\log_grid_grasp.txt"
    
    # Abre os arquivos de log
    with open(grid_log_file, 'w', newline='') as csv_file, open(text_log_file, 'w') as txt_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Dataset Size", "Alpha", "Iterations", "Result"])
        
        # Gerando todas as combinações possíveis de hiperparâmetros
        for dataset_size, alpha, iterations in itertools.product(dataset_sizes, alphas, iterations_list):
            log_message = f"Running GRASP with dataset_size={dataset_size}, alpha={alpha:.2f}, iterations={iterations}"
            print(log_message)  # Exibe no terminal
            txt_file.write(log_message + '\n')  # Salva no arquivo de texto
            
            # Chama o algoritmo GRASP
            run_grasp(dataset_size, alpha, iterations)
            
            # Lê o valor do log
            log_value = read_log_value(dataset_size, alpha, iterations)
            
            # Escreve os resultados no CSV
            csv_writer.writerow([dataset_size, f"{alpha:.2f}", iterations, log_value])
            
            # Atualiza os melhores parâmetros
            if log_value is not None and log_value < best_value:
                best_value = log_value
                best_params = (dataset_size, alpha, iterations)
        
        # Escreve o melhor resultado no final do CSV
        csv_writer.writerow([])
        csv_writer.writerow(["Best Result"])
        csv_writer.writerow(["Dataset Size", "Alpha", "Iterations", "Result"])
        csv_writer.writerow([best_params[0], f"{best_params[1]:.2f}", best_params[2], best_value])
        
        # Também registra o melhor resultado no log de texto
        best_message = f"Best result: {best_value} with parameters: dataset_size={best_params[0]}, alpha={best_params[1]:.2f}, iterations={best_params[2]}"
        print(best_message)  # Exibe no terminal
        txt_file.write(best_message + '\n')  # Salva no arquivo de texto
    
    return best_params, best_value

# Definição dos intervalos e step sizes para os hiperparâmetros
dataset_sizes = [100]  # Apenas um valor fixo, 100
alphas = np.arange(0.00, 1.01, 0.01)  # Valores de alpha de 0.1 a 1.0 com passo 0.1
iterations_list = np.arange(1000, 10001, 3000)  # Valores de 1000 a 5000 com passo 1000

# Realizando o grid search
best_params, best_value = grid_search(dataset_sizes, alphas, iterations_list)
