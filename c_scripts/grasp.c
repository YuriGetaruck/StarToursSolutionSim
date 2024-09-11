#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h> // Para utilizar as funções sqrt() e pow()
#include <time.h> // Para gerar números aleatórios

#define ALPHA 0.3 // Parâmetro que controla a aleatoriedade da lista restrita de candidatos (0.0 é totalmente guloso, 1.0 é totalmente aleatório)

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

// Função para criar a matriz de distâncias
float **criarMatrizDistancias(CoordenadaEstrela *coordenadas, int tamanho)
{
    float **matrizDistancias = (float **)malloc(tamanho * sizeof(float *));
    for (int i = 0; i < tamanho; i++)
    {
        matrizDistancias[i] = (float *)malloc(tamanho * sizeof(float));
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

// Função para encontrar o próximo ponto mais próximo não visitado, com base em uma lista restrita de candidatos (RCL)
int encontrarProximoPontoRCL(float **matrizDistancias, bool *visitado, int pontoAtual, int tamanho)
{
    int candidatos[tamanho];
    int numCandidatos = 0;
    float distMin = INFINITY, distMax = 0;

    // Encontrar a menor e maior distância dos pontos não visitados
    for (int i = 0; i < tamanho; i++)
    {
        if (!visitado[i] && i != pontoAtual)
        {
            float dist = matrizDistancias[pontoAtual][i];
            if (dist < distMin)
                distMin = dist;
            if (dist > distMax)
                distMax = dist;
        }
    }

    // Definir limite de inclusão na lista restrita de candidatos (RCL)
    float limite = distMin + ALPHA * (distMax - distMin);

    // Construir a lista restrita de candidatos (RCL)
    for (int i = 0; i < tamanho; i++)
    {
        if (!visitado[i] && i != pontoAtual)
        {
            float dist = matrizDistancias[pontoAtual][i];
            if (dist <= limite)
            {
                candidatos[numCandidatos++] = i;
            }
        }
    }

    // Escolher um ponto aleatório da lista restrita
    int escolhido = candidatos[rand() % numCandidatos];
    return escolhido;
}

// Função para calcular a distância total de uma solução
float calcularDistanciaTotal(int *caminho, float **matrizDistancias, int tamanho)
{
    float distanciaTotal = 0.0;
    for (int i = 0; i < tamanho - 1; i++)
    {
        distanciaTotal += matrizDistancias[caminho[i]][caminho[i + 1]];
    }
    // Fechar o ciclo
    distanciaTotal += matrizDistancias[caminho[tamanho - 1]][caminho[0]];
    return distanciaTotal;
}

// Fase construtiva do GRASP
void faseConstrutivaGRASP(CoordenadaEstrela *coordenadas, float **matrizDistancias, int tamanho, int *caminho, float *distanciaTotal)
{
    bool *visitado = (bool *)calloc(tamanho, sizeof(bool));
    int pontoAtual = rand() % tamanho; // Começa em um ponto aleatório
    visitado[pontoAtual] = true;
    caminho[0] = pontoAtual;

    for (int i = 1; i < tamanho; i++)
    {
        int proximoPonto = encontrarProximoPontoRCL(matrizDistancias, visitado, pontoAtual, tamanho);
        caminho[i] = proximoPonto;
        visitado[proximoPonto] = true;
        pontoAtual = proximoPonto;
    }

    free(visitado);

    *distanciaTotal = calcularDistanciaTotal(caminho, matrizDistancias, tamanho);
}

// Função de busca local (2-opt)
void buscaLocal2Opt(int *caminho, float **matrizDistancias, int tamanho, float *distanciaTotal)
{
    bool melhorou = true;
    while (melhorou)
    {
        melhorou = false;
        for (int i = 0; i < tamanho - 1; i++)
        {
            for (int j = i + 1; j < tamanho; j++)
            {
                // Testa a troca de dois segmentos
                int novoCaminho[tamanho];
                for (int k = 0; k < i; k++)
                    novoCaminho[k] = caminho[k];
                for (int k = i, l = j; k <= j; k++, l--)
                    novoCaminho[k] = caminho[l];
                for (int k = j + 1; k < tamanho; k++)
                    novoCaminho[k] = caminho[k];

                float novaDistancia = calcularDistanciaTotal(novoCaminho, matrizDistancias, tamanho);
                if (novaDistancia < *distanciaTotal)
                {
                    // Atualiza o caminho e a distância
                    for (int k = 0; k < tamanho; k++)
                        caminho[k] = novoCaminho[k];
                    *distanciaTotal = novaDistancia;
                    melhorou = true;
                }
            }
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Uso: %s <nomeArquivo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    srand(time(NULL)); // Inicializa o gerador de números aleatórios

    char nomeArquivo[256];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "datasets/%s", argv[1]);

    int tamanho = atoi(argv[2]);
    CoordenadaEstrela *coordenadas = (CoordenadaEstrela *)malloc(tamanho * sizeof(CoordenadaEstrela));

    coordenadas = lerCoordenadas(nomeArquivo, &tamanho);
    float **matrizDistancias = criarMatrizDistancias(coordenadas, tamanho);

    int melhorCaminho[tamanho];
    float melhorDistancia = INFINITY;

    for (int iteracao = 0; iteracao < 100; iteracao++)
    {
        int caminho[tamanho];
        float distanciaTotal;

        // Fase construtiva
        faseConstrutivaGRASP(coordenadas, matrizDistancias, tamanho, caminho, &distanciaTotal);

        // Busca local
        buscaLocal2Opt(caminho, matrizDistancias, tamanho, &distanciaTotal);

        // Atualiza o melhor caminho
        if (distanciaTotal < melhorDistancia)
        {
            melhorDistancia = distanciaTotal;
            for (int i = 0; i < tamanho; i++)
            {
                melhorCaminho[i] = caminho[i];
            }
        }
    }

    printf("Melhor caminho encontrado: [");
    for (int i = 0; i < tamanho; i++)
    {
        if (i < tamanho - 1)
            printf("%d, ", melhorCaminho[i]);
        else
            printf("%d", melhorCaminho[i]);
    }
    printf("]\nDistância total: %.2f\n", melhorDistancia);

    liberarMatrizDistancias(matrizDistancias, tamanho);
    free(coordenadas);

    return 0;
}
