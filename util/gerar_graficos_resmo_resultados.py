import matplotlib.pyplot as plt

# Dados
estrelas = [100, 1000, 10000, 37859]
nn = [17.46, 14.26, 12.15, 16.06]
grasp = [0.10, 4.80, 7.14, 7.53]
ga = [2.33, 16.36, 916.60, 3004.82]
aco = [1.42, 10.39, 14.43, 460.62]

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.plot(estrelas, nn, marker='o', label="NN")
plt.plot(estrelas, grasp, marker='o', label="GRASP")
plt.plot(estrelas, ga, marker='o', label="GA")
plt.plot(estrelas, aco, marker='o', label="ACO")

# Configurações do gráfico
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Estrelas", fontsize=12)
plt.ylabel("% Maior que o Ótimo", fontsize=12)
plt.title("Comparação de Desempenho - Algoritmos TSP", fontsize=14)
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

# Exibindo o gráfico
plt.show()


#Sempre exibir os detalhes
# Dados para % Melhor que Aleatório

nn_better = [69.75, 87.01, 94.06, 96.57]

grasp_better = [74.22, 88.08, 94.32, 96.82]

ga_better = [73.65, 86.77, 46.12, 8.31]

aco_better = [73.89, 87.45, 93.94, 83.44]



# Criando o gráfico

plt.figure(figsize=(10, 6))

plt.plot(estrelas, nn_better, marker='o', label="NN")

plt.plot(estrelas, grasp_better, marker='o', label="GRASP")

plt.plot(estrelas, ga_better, marker='o', label="GA")

plt.plot(estrelas, aco_better, marker='o', label="ACO")



# Configurações do gráfico

plt.xscale('log')

plt.xlabel("Estrelas", fontsize=12)

plt.ylabel("% Melhor que Aleatório", fontsize=12)

plt.title("Comparação de Desempenho - Algoritmos TSP", fontsize=14)

plt.legend()

plt.grid(True, which="both", linestyle="--", linewidth=0.5)

plt.tight_layout()



# Exibindo o gráfico

plt.show()