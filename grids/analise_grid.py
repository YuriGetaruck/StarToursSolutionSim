import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações do Seaborn para melhorar a estética dos gráficos
sns.set(style="whitegrid")

# Carregando os dados do CSV
file_path = "log_grid_aco.csv"  # Substitua pelo caminho do seu arquivo CSV
data = pd.read_csv(file_path)

# Separando o melhor resultado
best_result = data[data['Dataset Size'] == 'Best Result']
data = data[data['Dataset Size'] != 'Best Result']

# Convertendo os dados para os tipos corretos
data = data.astype({
    "Dataset Size": int,
    "Number of Ants": int,
    "Alpha": float,
    "Beta": float,
    "Evaporation": float,
    "Q": int,
    "Iterations": int,
    "Result": float
})

# Função para gerar gráficos de análise
def plot_results(data, x_param, hue_param, title):
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=data,
        x=x_param,
        y="Result",
        hue=hue_param,
        marker="o"
    )
    plt.title(title, fontsize=16)
    plt.xlabel(x_param, fontsize=14)
    plt.ylabel("Result (Objective Function Value)", fontsize=14)
    plt.legend(title=hue_param)
    plt.tight_layout()
    plt.show()

# Gráficos específicos
plot_results(data, x_param="Q", hue_param="Evaporation", title="Impacto de Q e Evaporation no Resultado")
plot_results(data, x_param="Alpha", hue_param="Beta", title="Impacto de Alpha e Beta no Resultado")
plot_results(data, x_param="Number of Ants", hue_param="Dataset Size", title="Impacto do Número de Formigas e Tamanho do Dataset")

# Destaque do melhor resultado
plt.figure(figsize=(6, 4))
best_result_row = best_result.iloc[0]
plt.barh(
    y=["Best Result"],
    width=[best_result_row["Result"]],
    color="green"
)
plt.title("Melhor Resultado Obtido", fontsize=16)
plt.xlabel("Resultado (Objective Function Value)", fontsize=14)
plt.tight_layout()
plt.show()
