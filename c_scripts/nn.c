#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>

// Estrutura para representar uma coordenada
typedef struct
{
    int id;
    float x;
    float y;
    float z;
} CoordenadaEstrela;

FILE *create_log_file(int tamanho)
{
    // Nome do diretório
    const char *directory = "c_scripts/logs";

    // Buffer para o nome do arquivo
    char filename[100];
    sprintf(filename, "%s/log_nn_%d.txt", directory, tamanho);

    // Criar e abrir o arquivo
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        perror("Erro ao criar o arquivo");
        return NULL;
    }

    return file;
}

// Função para salvar informações no arquivo de log
void save_log(FILE *file, int iteracao, double distancia_total, double tempo_decorrido)
{
    if (file == NULL)
    {
        perror("Arquivo não está aberto");
        return;
    }

    fprintf(file, "%d,%.2f,%.3f\n", iteracao, distancia_total, tempo_decorrido);
    fflush(file);
}

// Função para calcular a distância entre dois pontos em 3D
float calcularDistancia(CoordenadaEstrela ponto1, CoordenadaEstrela ponto2)
{
    float distancia;
    distancia = sqrt(pow(ponto2.x - ponto1.x, 2) + pow(ponto2.y - ponto1.y, 2) + pow(ponto2.z - ponto1.z, 2));
    return distancia;
}

// Função para criar a matriz de distâncias
float **criarMatrizDistancias(CoordenadaEstrela *coordenadas, int tamanho)
{
    float **matrizDistancias = (float **)malloc(tamanho * sizeof(float *));
    if (matrizDistancias == NULL)
    {
        printf("Erro ao alocar memória para matrizDistancias\n");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < tamanho; i++)
    {
        matrizDistancias[i] = (float *)malloc(tamanho * sizeof(float));
        if (matrizDistancias[i] == NULL)
        {
            printf("Erro ao alocar memória para matrizDistancias\n");
            exit(EXIT_FAILURE);
        }

        for (int j = 0; j <= i; j++)  // Apenas abaixo ou na diagonal principal
        {
            if (i == j)
            {
                matrizDistancias[i][j] = 0.0f;  // Distância para si mesmo é zero
            }
            else
            {
                matrizDistancias[i][j] = calcularDistancia(coordenadas[i], coordenadas[j]);
                matrizDistancias[j][i] = matrizDistancias[i][j];  // Preenche a parte superior
            }
        }
    }

    return matrizDistancias;
}

// Função para liberar a matriz de distâncias
void liberarMatrizDistancias(float **matrizDistancias, int tamanho)
{
    for (int i = 0; i < tamanho; i++)
    {
        free(matrizDistancias[i]);
    }
    free(matrizDistancias);
}

// Função para percorrer o vetor de coordenadas e calcular a distância total entre estrelas consecutivas
float calcularDistanciaTotal(CoordenadaEstrela *coordenadas, int tamanho)
{
    float distanciaTotal = 0.0;
    for (int i = 0; i < tamanho - 1; i += 2)
    {
        distanciaTotal += calcularDistancia(coordenadas[i], coordenadas[i + 1]);
    }

    distanciaTotal += calcularDistancia(coordenadas[tamanho - 1], coordenadas[0]);
    return distanciaTotal;
}

// Função para encontrar o próximo ponto mais próximo não visitado
int encontrarProximoPontoMaisProximo(float **matrizDistancias, bool *visitado, int pontoAtual, int tamanho)
{
    int proximoPonto = -1;
    float menorDistancia = INFINITY;

    for (int i = 0; i < tamanho; i++)
    {
        if (!visitado[i] && i != pontoAtual)
        {
            float distancia = matrizDistancias[pontoAtual][i];
            if (distancia < menorDistancia)
            {
                menorDistancia = distancia;
                proximoPonto = i;
            }
        }
    }

    return proximoPonto;
}

// ALGORITMO GULOSO
// Função para encontrar a rota usando o algoritmo guloso
void algoritmoGulosoVizinhoMaisProximo(CoordenadaEstrela *coordenadas, float **matrizDistancias, int tamanho, int *caminho, float *distanciaTotal, clock_t inicio, FILE *log_file)
{
    bool *visitado = (bool *)calloc(tamanho, sizeof(bool));
    int pontoAtual = 0;

    visitado[pontoAtual] = true;
    caminho[0] = coordenadas[pontoAtual].id;

    *distanciaTotal = 0.0;

    for (int i = 1; i < tamanho; i++)
    {
        int proximoPonto = encontrarProximoPontoMaisProximo(matrizDistancias, visitado, pontoAtual, tamanho);
        caminho[i] = coordenadas[proximoPonto].id;
        *distanciaTotal += matrizDistancias[pontoAtual][proximoPonto];
        visitado[proximoPonto] = true;
        pontoAtual = proximoPonto; // Atualizando o ponto atual para o próximo ponto selecionado
        clock_t autal = clock();
        double tempo_decorrido = (double)(autal - inicio) / CLOCKS_PER_SEC;
        save_log(log_file, i, *distanciaTotal, tempo_decorrido);
    }

    *distanciaTotal += matrizDistancias[pontoAtual][0];
    caminho[tamanho + 1] = coordenadas[0].id;
    clock_t autal = clock();
    double tempo_decorrido = (double)(autal - inicio) / CLOCKS_PER_SEC;
    save_log(log_file, tamanho, *distanciaTotal, tempo_decorrido);

    free(visitado);
}

// Função para extrair coordenadas
CoordenadaEstrela *lerCoordenadas(const char *nomeArquivo, int *tamanho)
{
    FILE *arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL)
    {
        perror("Erro ao abrir o arquivo");
        exit(EXIT_FAILURE);
    }

    // Contar o número de linhas no arquivo
    int linhas = 0;
    float dummy_x, dummy_y, dummy_z;
    while (fscanf(arquivo, "%f %f %f", &dummy_x, &dummy_y, &dummy_z) == 3)
    {
        linhas++;
    }

    rewind(arquivo); // Voltar ao início do arquivo

    // Alocar dinamicamente o vetor de coordenadas
    CoordenadaEstrela *coordenadas = (CoordenadaEstrela *)malloc(linhas * sizeof(CoordenadaEstrela));
    if (coordenadas == NULL)
    {
        perror("Erro ao alocar memória");
        exit(EXIT_FAILURE);
    }

    // Ler as coordenadas e armazenar no vetor
    for (int i = 0; i < linhas; i++)
    {
        if (fscanf(arquivo, "%f %f %f", &coordenadas[i].x, &coordenadas[i].y, &coordenadas[i].z) != 3)
        {
            fprintf(stderr, "Erro ao ler coordenadas do arquivo\n");
            exit(EXIT_FAILURE);
        }
        coordenadas[i].id = i + 1;
    }

    fclose(arquivo);

    // Definir o tamanho do vetor
    *tamanho = linhas;

    // Retornar o vetor de coordenadas
    return coordenadas;
}

int main(int argc, char *argv[])
{
    clock_t inicio = clock();

    // Verifica se o nome do arquivo foi passado como argumento
    if (argc < 2)
    {
        fprintf(stderr, "Uso: %s <nomeArquivo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char nomeArquivo[256];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "datasets/%s", argv[1]);

    int tamanho = atoi(argv[2]);
    if (tamanho <= 0)
    {
        fprintf(stderr, "Tamanho inválido: %s\n", argv[2]);
        return EXIT_FAILURE;
    }
    FILE *log_file = create_log_file(tamanho);
    CoordenadaEstrela *coordenadas = (CoordenadaEstrela *)malloc(tamanho * sizeof(CoordenadaEstrela));

    if (coordenadas == NULL)
    {
        fprintf(stderr, "Erro ao alocar memória para coordenadas.\n");
        return EXIT_FAILURE;
    }

    coordenadas = lerCoordenadas(nomeArquivo, &tamanho);

    float **matrizDistancias = criarMatrizDistancias(coordenadas, tamanho);

    int caminho[tamanho + 1];
    float distanciaGuloso;

    algoritmoGulosoVizinhoMaisProximo(coordenadas, matrizDistancias, tamanho, caminho, &distanciaGuloso, inicio, log_file);

    // Imprime o caminho
    printf("[");
    for (int i = 0; i < tamanho; i++)
    {
        if (i < tamanho - 1)
        {
            printf("%d, ", caminho[i] - 1);
        }
        else
        {
            printf("%d", caminho[i] - 1);
        }
    }
    printf(", 0]");

    liberarMatrizDistancias(matrizDistancias, tamanho);
    free(coordenadas);

    return 0;
}
