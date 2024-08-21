#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <float.h>
#include <time.h>

// Estrutura para representar uma coordenada
typedef struct
{
    int id;
    float x;
    float y;
    float z;
} CoordenadaEstrela;

// Função para calcular a distância entre dois pontos em 3D
float calcularDistancia(CoordenadaEstrela ponto1, CoordenadaEstrela ponto2)
{
    return sqrt(pow(ponto2.x - ponto1.x, 2) + pow(ponto2.y - ponto1.y, 2) + pow(ponto2.z - ponto1.z, 2));
}

// Função para criar a matriz de distâncias
float **criarMatrizDistancias(CoordenadaEstrela *coordenadas, int tamanho)
{
    float **matrizDistancias = (float **)malloc(tamanho * sizeof(float *));
    if (matrizDistancias == NULL)
    {
        printf("Erro ao alocar memória para matrizDistancias");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < tamanho; i++)
    {
        matrizDistancias[i] = (float *)malloc(tamanho * sizeof(float));
        if (matrizDistancias[i] == NULL)
        {
            printf("Erro ao alocar memória para matrizDistancias[%d]", i);
            exit(EXIT_FAILURE);
        }
        for (int j = 0; j < tamanho; j++)
        {
            matrizDistancias[i][j] = calcularDistancia(coordenadas[i], coordenadas[j]);
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

// Função para calcular a distância total de um caminho
float calcularDistanciaTotal(int *caminho, float **matrizDistancias, int tamanho)
{
    float distanciaTotal = 0.0;
    for (int i = 0; i < tamanho - 2; i++)
    {
        distanciaTotal += matrizDistancias[caminho[i]][caminho[i + 1]];
        printf("distanciatotal = %f\n", distanciaTotal);
    }
    distanciaTotal += matrizDistancias[caminho[tamanho - 1]][caminho[0]]; // Retorno ao ponto inicial
    return distanciaTotal;
}

// Função para encontrar o próximo ponto mais próximo não visitado
int encontrarProximoPontoMaisProximo(float **matrizDistancias, bool *visitado, int pontoAtual, int tamanho)
{
    int proximoPonto = -1;
    float menorDistancia = FLT_MAX;

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

// Função para realizar a busca local usando o 2-opt
void buscaLocal2Opt(int *caminho, float **matrizDistancias, int tamanho)
{
    printf(" 0 \n");
    bool melhora = true;
    while (melhora)
    {
        melhora = false;
        for (int i = 1; i < tamanho - 1; i++)
        {
            for (int j = i + 1; j < tamanho; j++)
            {
                // Troca duas arestas e calcula a nova distância total
                int tmp = caminho[i];
                caminho[i] = caminho[j];
                caminho[j] = tmp;

                printf(" 1 \n");

                float novaDistancia = calcularDistanciaTotal(caminho, matrizDistancias, tamanho);
                float antigaDistancia = calcularDistanciaTotal(caminho, matrizDistancias, tamanho);

                if (novaDistancia < antigaDistancia)
                {
                    printf(" 2 \n");

                    melhora = true;
                }
                else
                {
                    // Reverter a troca se não houver melhora
                    printf(" 3 \n");
                    tmp = caminho[i];
                    caminho[i] = caminho[j];
                    caminho[j] = tmp;
                }
            }
        }
    }
}

// Função para encontrar a rota inicial usando uma estratégia gulosa aleatória
void construcaoGulosaAleatoria(CoordenadaEstrela *coordenadas, float **matrizDistancias, int tamanho, int *caminho, float *distanciaTotal)
{
    bool *visitado = (bool *)calloc(tamanho, sizeof(bool));
    int pontoAtual = 0;
    visitado[pontoAtual] = true;
    caminho[0] = coordenadas[pontoAtual].id;

    *distanciaTotal = 0.0;

    for (int i = 1; i < tamanho; i++)
    {
        int proximoPonto;
        int candidatos[tamanho];
        int numCandidatos = 0;
        float alpha = 0.3; // Parâmetro de aleatoriedade

        // Construir lista de candidatos
        for (int j = 0; j < tamanho; j++)
        {
            if (!visitado[j] && j != pontoAtual)
            {
                candidatos[numCandidatos++] = j;
            }
        }

        // Selecionar próximo ponto aleatoriamente dentre os candidatos
        proximoPonto = candidatos[rand() % numCandidatos];

        caminho[i] = coordenadas[proximoPonto].id;
        *distanciaTotal += matrizDistancias[pontoAtual][proximoPonto];
        visitado[proximoPonto] = true;
        pontoAtual = proximoPonto;
    }

    *distanciaTotal += matrizDistancias[pontoAtual][0];
    caminho[tamanho] = coordenadas[0].id;

    free(visitado);
}

// Função para executar o algoritmo GRASP
void algoritmoGRASP(CoordenadaEstrela *coordenadas, float **matrizDistancias, int tamanho, int *melhorCaminho, float *melhorDistancia)
{
    int iteracoes = 100;
    *melhorDistancia = FLT_MAX;

    for (int i = 0; i < iteracoes; i++)
    {
        int caminho[tamanho + 1];
        float distanciaAtual;

        // Construção da solução inicial
        construcaoGulosaAleatoria(coordenadas, matrizDistancias, tamanho, caminho, &distanciaAtual);
        printf("CONST GULOSA");

        // Busca local com 2-opt
        buscaLocal2Opt(caminho, matrizDistancias, tamanho);
        printf("2opt");

        // Atualiza o melhor caminho encontrado
        float distanciaFinal = calcularDistanciaTotal(caminho, matrizDistancias, tamanho);
        if (distanciaFinal < *melhorDistancia)
        {
            *melhorDistancia = distanciaFinal;
            for (int j = 0; j < tamanho; j++)
            {
                melhorCaminho[j] = caminho[j];
            }
        }
    }
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

    *tamanho = linhas;
    return coordenadas;
}

int main(int argc, char *argv[])
{
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

    CoordenadaEstrela *coordenadas = lerCoordenadas(nomeArquivo, &tamanho);
    float **matrizDistancias = criarMatrizDistancias(coordenadas, tamanho);

    int melhorCaminho[tamanho + 1];
    float melhorDistancia;

    srand(time(NULL)); // Inicializa o gerador de números aleatórios

    algoritmoGRASP(coordenadas, matrizDistancias, tamanho, melhorCaminho, &melhorDistancia);

    printf("Melhor caminho: [");
    for (int i = 0; i < tamanho; i++)
    {
        if (i < tamanho - 1)
        {
            printf("%d, ", melhorCaminho[i] - 1);
        }
        else
        {
            printf("%d", melhorCaminho[i] - 1);
        }
    }
    printf("]\n");

    printf("Menor distância encontrada: %f\n", melhorDistancia);

    liberarMatrizDistancias(matrizDistancias, tamanho);
    free(coordenadas);

    return 0;
}