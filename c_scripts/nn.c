#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h> // Para utilizar as funções sqrt() e pow()

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
    float distancia;
    distancia = sqrt(pow(ponto2.x - ponto1.x, 2) + pow(ponto2.y - ponto1.y, 2) + pow(ponto2.z - ponto1.z, 2));
    return distancia;
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
int encontrarProximoPontoMaisProximo(CoordenadaEstrela *coordenadas, bool *visitado, int pontoAtual, int tamanho)
{
    int proximoPonto = -1;
    float menorDistancia = INFINITY;

    for (int i = 0; i < tamanho; i++)
    {
        if (!visitado[i] && i != pontoAtual)
        {
            float distancia = calcularDistancia(coordenadas[pontoAtual], coordenadas[i]);
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
void algoritmoGulosoVizinhoMaisProximo(CoordenadaEstrela *coordenadas, int tamanho, int *caminho, float *distanciaTotal)
{
    bool *visitado = (bool *)calloc(tamanho, sizeof(bool));
    int pontoAtual = 0;

    visitado[pontoAtual] = true;
    caminho[0] = coordenadas[pontoAtual].id;

    *distanciaTotal = 0.0;

    for (int i = 1; i < tamanho; i++)
    {
        int proximoPonto = encontrarProximoPontoMaisProximo(coordenadas, visitado, pontoAtual, tamanho);
        caminho[i] = coordenadas[proximoPonto].id;
        *distanciaTotal += calcularDistancia(coordenadas[pontoAtual], coordenadas[proximoPonto]);
        visitado[proximoPonto] = true;
        pontoAtual = proximoPonto; // Atualizando o ponto atual para o próximo ponto selecionado
    }

    *distanciaTotal += calcularDistancia(coordenadas[pontoAtual], coordenadas[0]);
    caminho[tamanho + 1] = coordenadas[0].id;

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
    // Verifica se o nome do arquivo foi passado como argumento
    if (argc < 2)
    {
        fprintf(stderr, "Uso: %s <nomeArquivo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char nomeArquivo[256];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "..\\datasets\\%s", argv[1]);

    int tamanho = atoi(argv[2]);
    if (tamanho <= 0)
    {
        fprintf(stderr, "Tamanho inválido: %s\n", argv[2]);
        return EXIT_FAILURE;
    }
    CoordenadaEstrela *coordenadas = (CoordenadaEstrela *)malloc(tamanho * sizeof(CoordenadaEstrela));

    if (coordenadas == NULL)
    {
        fprintf(stderr, "Erro ao alocar memória para coordenadas.\n");
        return EXIT_FAILURE;
    }

    coordenadas = lerCoordenadas(nomeArquivo, &tamanho);

    int caminho[tamanho + 1];
    float distanciaGuloso;

    algoritmoGulosoVizinhoMaisProximo(coordenadas, tamanho, caminho, &distanciaGuloso);

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

    free(coordenadas);

    return 0;
}
