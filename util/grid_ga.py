import subprocess
import os
import csv
import itertools
import numpy as np

# Função para ler o valor do log CSV
def read_log_value(dataset_size, mutation_rate, population, iterations):
    mutation_rate_formatted = f"{mutation_rate:.2f}"
    
    log_filename = f"c_scripts\\logs\\log_ga_{dataset_size}_{mutation_rate_formatted}_{population}_{iterations}.txt"
    
    if not os.path.exists(log_filename):
        print(f"Log file {log_filename} not found.")
        return None
    
    # Lê o arquivo e verifica se ele possui linhas
    with open(log_filename, 'r') as file:
        reader = list(csv.reader(file))
        if not reader:  # Verifica se está vazio
            print(f"Log file {log_filename} is empty.")
            return None
        
        # Retorna a segunda coluna da última linha
        last_row = reader[-1]
        if len(last_row) < 2:  # Verifica se há ao menos 2 colunas
            print(f"Log file {log_filename} has insufficient columns.")
            return None
        
        return float(last_row[1])


# Função para chamar o algoritmo genético em C
def run_ga(dataset_size, mutation_rate, population, iterations):
    args = ["c_scripts\\ga.exe", "star100.xyz.txt", str(dataset_size), str(mutation_rate), str(population), str(iterations)]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout

# Função para realizar o grid search
def grid_search(dataset_sizes, mutation_rates, populations, iterations_list):
    best_value = float('inf')
    best_params = None
    
    # Certifique-se de que as pastas "grids" e "logs" existem
    os.makedirs("grids", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Nome dos arquivos de log
    grid_log_file = "grids\\log_grid_ga.csv"
    text_log_file = "logs\\log_grid_ga.txt"
    
    # Abre os arquivos de log
    with open(grid_log_file, 'w', newline='') as csv_file, open(text_log_file, 'w') as txt_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Dataset Size", "Mutation Rate", "Population", "Iterations", "Result"])
        
        # Gerando todas as combinações possíveis de hiperparâmetros
        for dataset_size, mutation_rate, population, iterations in itertools.product(dataset_sizes, mutation_rates, populations, iterations_list):
            log_message = f"Running GA with dataset_size={dataset_size}, mutation_rate={mutation_rate:.2f}, population={population}, iterations={iterations}"
            print(log_message)  # Exibe no terminal
            txt_file.write(log_message + '\n')  # Salva no arquivo de texto
            
            # Chama o algoritmo genético
            run_ga(dataset_size, mutation_rate, population, iterations)
            
            # Lê o valor do log
            log_value = read_log_value(dataset_size, mutation_rate, population, iterations)
            
            # Escreve os resultados no CSV
            csv_writer.writerow([dataset_size, f"{mutation_rate:.2f}", population, iterations, log_value])
            
            # Atualiza os melhores parâmetros
            if log_value is not None and log_value < best_value:
                best_value = log_value
                best_params = (dataset_size, mutation_rate, population, iterations)
        
        # Escreve o melhor resultado no final do CSV
        csv_writer.writerow([])
        csv_writer.writerow(["Best Result"])
        csv_writer.writerow(["Dataset Size", "Mutation Rate", "Population", "Iterations", "Result"])
        csv_writer.writerow([best_params[0], f"{best_params[1]:.2f}", best_params[2], best_params[3], best_value])
        
        # Também registra o melhor resultado no log de texto
        best_message = f"Best result: {best_value} with parameters: dataset_size={best_params[0]}, mutation_rate={best_params[1]:.2f}, population={best_params[2]}, iterations={best_params[3]}"
        print(best_message)  # Exibe no terminal
        txt_file.write(best_message + '\n')  # Salva no arquivo de texto
    
    return best_params, best_value

# Definição dos intervalos e step sizes para os hiperparâmetros
dataset_sizes = [100]  # Apenas um valor fixo, 100
mutation_rates = np.arange(0.01, 0.25, 0.01)  # Valores de 0.01 a 0.15 com passo 0.01
populations = np.arange(50, 251, 50)  # Valores de 50 a 150 com passo 10
iterations_list = np.arange(1000, 10001, 3000)  # Valores de 1000 a 5000 com passo 1000

# Realizando o grid search
best_params, best_value = grid_search(dataset_sizes, mutation_rates, populations, iterations_list)
