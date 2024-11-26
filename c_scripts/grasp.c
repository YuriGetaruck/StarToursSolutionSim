#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include <time.h>

// Estrutura para representar uma coordenada
typedef struct
{
    int id;
    float x;
    float y;
    float z;
} CoordenadaEstrela;

FILE *create_log_file(int tamanho, double alpha, int iteracoes)
{
    // Nome do diretório
    const char *directory = "c_scripts/logs";

    // Buffer para o nome do arquivo
    char filename[100];
    sprintf(filename, "%s/log_grasp_%d_%.2f_%d.txt", directory, tamanho, alpha, iteracoes);

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
    return sqrtf(powf(ponto2.x - ponto1.x, 2) +
                 powf(ponto2.y - ponto1.y, 2) +
                 powf(ponto2.z - ponto1.z, 2));
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

        for (int j = 0; j < i; j++)  // Calcula apenas abaixo da diagonal principal
        {
            matrizDistancias[i][j] = calcularDistancia(coordenadas[i], coordenadas[j]);
            matrizDistancias[j][i] = matrizDistancias[i][j];  // Preenche a parte de cima da diagonal
        }
        matrizDistancias[i][i] = 0.0f;  // A distância de uma estrela para ela mesma é 0
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

// Função para calcular a distância total de um caminho
float calcularDistanciaTotal(int *caminho, float **matrizDistancias, int tamanho)
{
    float distanciaTotal = 0.0f;
    for (int i = 0; i < tamanho - 1; i++)
    {
        distanciaTotal += matrizDistancias[caminho[i]][caminho[i + 1]];
    }
    distanciaTotal += matrizDistancias[caminho[tamanho - 1]][caminho[0]]; // Retorno ao início
    return distanciaTotal;
}

// Função para ler coordenadas do arquivo
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
        coordenadas[i].id = i;
    }

    fclose(arquivo);

    // Definir o tamanho do vetor
    *tamanho = linhas;

    // Retornar o vetor de coordenadas
    return coordenadas;
}

// Função para construir uma solução inicial usando GRASP (RCL)
int *construirSolucao(float **matrizDistancias, int tamanho, float alpha)
{
    int *solucao = (int *)malloc(tamanho * sizeof(int));
    if (solucao == NULL)
    {
        perror("Erro ao alocar memória para solução");
        exit(EXIT_FAILURE);
    }

    bool *visitado = (bool *)calloc(tamanho, sizeof(bool));
    if (visitado == NULL)
    {
        perror("Erro ao alocar memória para visitado");
        exit(EXIT_FAILURE);
    }

    int current = rand() % tamanho; // Ponto de partida aleatório
    solucao[0] = current;
    visitado[current] = true;

    for (int i = 1; i < tamanho; i++)
    {
        // Criar a lista de candidatos não visitados
        float minDist = INFINITY, maxDist = 0.0f;
        for (int j = 0; j < tamanho; j++)
        {
            if (!visitado[j])
            {
                if (matrizDistancias[current][j] < minDist)
                {
                    minDist = matrizDistancias[current][j];
                }
                if (matrizDistancias[current][j] > maxDist)
                {
                    maxDist = matrizDistancias[current][j];
                }
            }
        }

        // Definir o limiar para RCL
        float limite = minDist + alpha * (maxDist - minDist);

        // Construir RCL
        int *rcl = (int *)malloc(tamanho * sizeof(int));
        if (rcl == NULL)
        {
            perror("Erro ao alocar memória para RCL");
            exit(EXIT_FAILURE);
        }
        int rclSize = 0;
        for (int j = 0; j < tamanho; j++)
        {
            if (!visitado[j] && matrizDistancias[current][j] <= limite)
            {
                rcl[rclSize++] = j;
            }
        }

        if (rclSize == 0)
        { // Caso não haja candidatos na RCL, considerar todos não visitados
            for (int j = 0; j < tamanho; j++)
            {
                if (!visitado[j])
                {
                    rcl[rclSize++] = j;
                }
            }
        }

        // Selecionar aleatoriamente um candidato da RCL
        int selecionado = rcl[rand() % rclSize];
        solucao[i] = selecionado;
        visitado[selecionado] = true;
        current = selecionado;

        free(rcl);
    }

    free(visitado);
    return solucao;
}

// Função para realizar a troca 2-Opt
bool aplicar2Opt(int *solucao, float **matrizDistancias, int tamanho, float *distanciaTotal)
{
    bool melhorou = false;
    for (int i = 1; i < tamanho - 1; i++)
    {
        for (int j = i + 1; j < tamanho; j++)
        {
            // Cálculo das distâncias antes da troca
            float d1 = matrizDistancias[solucao[i - 1]][solucao[i]] + matrizDistancias[solucao[j]][solucao[(j + 1) % tamanho]];
            // Cálculo das distâncias depois da troca
            float d2 = matrizDistancias[solucao[i - 1]][solucao[j]] + matrizDistancias[solucao[i]][solucao[(j + 1) % tamanho]];
            if (d2 < d1)
            {
                // Realizar a troca
                for (int k = 0; k < (j - i + 1) / 2; k++)
                {
                    int temp = solucao[i + k];
                    solucao[i + k] = solucao[j - k];
                    solucao[j - k] = temp;
                }
                *distanciaTotal = *distanciaTotal - d1 + d2;
                melhorou = true;
            }
        }
    }
    return melhorou;
}

// Função de busca local 2-Opt
void buscaLocal2Opt(int *solucao, float **matrizDistancias, int tamanho, float *distanciaTotal)
{
    bool melhorou;
    do
    {
        melhorou = aplicar2Opt(solucao, matrizDistancias, tamanho, distanciaTotal);
    } while (melhorou);
}

// Função para copiar uma solução
int *copiarSolucao(int *solucao, int tamanho)
{
    int *copia = (int *)malloc(tamanho * sizeof(int));
    if (copia == NULL)
    {
        perror("Erro ao alocar memória para cópia da solução");
        exit(EXIT_FAILURE);
    }
    memcpy(copia, solucao, tamanho * sizeof(int));
    return copia;
}

// Função para imprimir a solução
void imprimirSolucao(int *solucao, int tamanho, float distanciaTotal)
{
    printf("[");
    for (int i = 0; i < tamanho + 1; i++)
    {
        if (i < tamanho)
        {
            printf("%d, ", solucao[i]);
        }
    }
    printf("%d]", solucao[0]); // Retorno ao início
}

int main(int argc, char *argv[])
{
    clock_t inicio = clock();
    // Inicialização da semente para números aleatórios
    srand(42);


    // Verifica se os argumentos necessários foram passados
    if (argc < 4)
    {
        return EXIT_FAILURE;
    }

    char nomeArquivo[256];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "datasets/%s", argv[1]);

    int numIteracoes = atoi(argv[2]);
    if (numIteracoes <= 0)
    {
        fprintf(stderr, "Número de iterações inválido: %s\n", argv[2]);
        return EXIT_FAILURE;
    }

    float alpha = atof(argv[3]);
    if (alpha < 0.0f || alpha > 1.0f)
    {
        fprintf(stderr, "Alpha inválido: %f. Deve estar entre 0 e 1.\n", alpha);
        return EXIT_FAILURE;
    }

    int tamanho;
    CoordenadaEstrela *coordenadas = lerCoordenadas(nomeArquivo, &tamanho);

    float **matrizDistancias = criarMatrizDistancias(coordenadas, tamanho);

    // Variáveis para armazenar a melhor solução
    int *melhorSolucao = NULL;
    float melhorDistancia = INFINITY;

    FILE *log_file = create_log_file(tamanho, alpha, numIteracoes);

    // GRASP Iterativo
    for (int iter = 0; iter < numIteracoes; iter++)
    {
        // Construção da solução inicial
        int *solucao = construirSolucao(matrizDistancias, tamanho, alpha);

        // Cálculo da distância total
        float distancia = calcularDistanciaTotal(solucao, matrizDistancias, tamanho);

        // Busca Local
        buscaLocal2Opt(solucao, matrizDistancias, tamanho, &distancia);

        // Atualização da melhor solução
        if (distancia < melhorDistancia)
        {
            if (melhorSolucao != NULL)
            {
                free(melhorSolucao);
            }
            melhorSolucao = copiarSolucao(solucao, tamanho);
            melhorDistancia = distancia;
        }

        clock_t autal = clock();
        double tempo_decorrido = (double)(autal - inicio) / CLOCKS_PER_SEC;
        save_log(log_file, iter + 1, melhorDistancia, tempo_decorrido);

        free(solucao);
    }

    // Imprimir a melhor solução encontrada
    if (melhorSolucao != NULL)
    {
        imprimirSolucao(melhorSolucao, tamanho, melhorDistancia);
        free(melhorSolucao);
    }
    else
    {
        printf("Nenhuma solução encontrada.\n");
    }

    liberarMatrizDistancias(matrizDistancias, tamanho);
    free(coordenadas);

    return 0;
}
