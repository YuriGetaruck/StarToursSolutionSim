import matplotlib.pyplot as plt

# Valores de referência
optimal_distance = 120.5
nn_distance = 140.8

# Dados fictícios para o gráfico
x = range(10)
y = [i * 15 for i in x]

# Criando o gráfico
plt.plot(x, y, label="Algoritmo Exemplo")

# Personalizando o eixo Y para incluir os valores de referência
y_ticks = list(plt.yticks()[0])  # Obtém os ticks atuais do eixo Y
y_labels = [f"{tick:.1f}" for tick in y_ticks]  # Converte para strings

# Adiciona os valores de referência aos ticks e labels
if optimal_distance not in y_ticks:
    y_ticks.append(optimal_distance)
    y_labels.append(f"Ótima ({optimal_distance:.2f})")

if nn_distance not in y_ticks:
    y_ticks.append(nn_distance)
    y_labels.append(f"NN ({nn_distance:.2f})")

# Ordenando os ticks para manter consistência no eixo Y
sorted_ticks_labels = sorted(zip(y_ticks, y_labels))
y_ticks, y_labels = zip(*sorted_ticks_labels)

# Atualizando o eixo Y
plt.yticks(ticks=y_ticks, labels=y_labels)

# Configuração do gráfico
plt.axhline(y=optimal_distance, color='red', linestyle='--', label="Distância Ótima")
plt.axhline(y=nn_distance, color='purple', linestyle='--', label="Distância NN")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.title("Exemplo de Personalização do Eixo Y")
plt.show()
