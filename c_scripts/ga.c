#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

// Variaveis globais para gerarGrid

float mutation_rate = 0.05;
int pop_size = 30;
int iterations = 10000;
int n = 100;
float target_distance = 1800;

// Estrutura para representar um ponto 3D
typedef struct
{
    int id;
    double x;
    double y;
    double z;
} Point;

// Estrutura para representar um indivíduo (caminho)
typedef struct
{
    int path[1025];
    double fitness;
} Individual;

// Calcula a distância euclidiana entre dois pontos 3D
double distance(Point p1, Point p2)
{
    float distancia;
    distancia = sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2) + pow(p2.z - p1.z, 2));
    return distancia;
}

// Calcula o comprimento do caminho de um indivíduo
double calculate_fitness(Individual individual, Point points[])
{
    double length = 0.0;
    for (int i = 0; i < n - 1; i++)
    {
        length += distance(points[individual.path[i]], points[individual.path[i + 1]]);
    }
    length += distance(points[individual.path[n - 1]], points[individual.path[0]]); // fecha o ciclo
    return length;
}

// Inicializa uma população de indivíduos com caminhos aleatórios
void initialize_population(Individual population[], Point points[])
{
    // Loop através de cada indivíduo na população
    for (int i = 0; i < pop_size; i++)
    {
        // Inicializar caminho com ordem sequencial
        for (int j = 0; j < n; j++)
        {
            population[i].path[j] = j;
        }

        // Embaralhar os pontos exceto o primeiro (ponto de partida)
        for (int j = n - 1; j > 0; j--)
        {
            // Gerar um índice aleatório dentro do intervalo [0, j]
            int k = rand() % (j + 1);

            // Trocar os valores dos índices j e k (exceto para o ponto inicial)
            if (k != 0) // Não embaralhar o ponto de partida
            {
                int temp = population[i].path[j];
                population[i].path[j] = population[i].path[k];
                population[i].path[k] = temp;
            }
        }

        // Calcular o fitness do indivíduo
        population[i].fitness = calculate_fitness(population[i], points);
        // printf("%d FITNESS: %.2f \n", i, population[i].fitness);
    }
}

// Seleciona indivíduos para reprodução usando torneio binário
Individual tournament_selection(Individual population[])
{
    Individual parent1 = population[rand() % pop_size];
    Individual parent2 = population[rand() % pop_size];
    return (parent1.fitness < parent2.fitness) ? parent1 : parent2;
}

// Realiza o cruzamento entre dois indivíduos para gerar um novo indivíduo
Individual crossover(Individual parent1, Individual parent2, Point *points)
{
    int start = rand() % n;
    int end = rand() % n;
    if (start > end)
    {
        int temp = start;
        start = end;
        end = temp;
    }
    Individual child;
    for (int i = 0; i < n; i++)
    {
        if (i >= start && i <= end)
        {
            child.path[i] = parent1.path[i];
        }
        else
        {
            child.path[i] = -1;
        }
    }
    int index = 0;
    for (int i = 0; i < n; i++)
    {
        if (index == start)
        {
            index = end + 1;
        }
        int gene = parent2.path[i];
        if (child.path[index] == -1)
        {
            bool contains = false;
            for (int j = 0; j < n; j++)
            {
                if (child.path[j] == gene)
                {
                    contains = true;
                    break;
                }
            }
            if (!contains)
            {
                child.path[index++] = gene;
            }
        }
    }
    child.fitness = calculate_fitness(child, points);
    return child;
}

// Realiza mutação por deslocamento simples em um indivíduo
void mutate_deslocamento_simples(Individual *individual)
{
    if ((double)rand() / RAND_MAX < mutation_rate)
    {
        int start = rand() % (n - 1) + 1;  // Ignorar o ponto de partida
        int length = rand() % (n - start); // Comprimento do deslocamento

        int temp[n];
        memcpy(temp, individual->path, sizeof(temp)); // Copia o caminho atual

        // Desloca a sub-rota em 'length' posições
        for (int i = 0; i < length; i++)
            individual->path[start + i] = temp[start + length - i - 1];
    }
}

void mutate_plus(Individual *individual)
{
    if ((double)rand() / RAND_MAX < 0.1)
    {
        int num_reversals = rand() % 3 + 1; // Escolha aleatoriamente entre 1, 2 ou 3 índices para inverter
        for (int i = 0; i < num_reversals; i++)
        {
            int start = rand() % (n - 2) + 1; // Ignorar o ponto de partida e o último ponto
            int end = start + 1;
            int temp = individual->path[start];
            individual->path[start] = individual->path[end];
            individual->path[end] = temp;
        }
    }
}

// Realiza mutação em um indivíduo
void mutate(Individual *individual)
{
    if ((double)rand() / RAND_MAX < mutation_rate)
    {
        int start = rand() % (n - 1) + 1; // Ignorar o ponto de partida
        int end = rand() % (n - 1) + 1;   // Ignorar o ponto de partida
        if (start > end)
        {
            int temp = start;
            start = end;
            end = temp;
        }
        while (start < end)
        {
            int temp = individual->path[start];
            individual->path[start] = individual->path[end];
            individual->path[end] = temp;
            start++;
            end--;
        }
    }
}

// Evolui a população por uma geração e verifica o critério de parada
bool evolve_population(Individual population[], Point points[])
{
    Individual new_population[pop_size];
    for (int i = 0; i < pop_size; i++)
    {
        Individual parent1 = tournament_selection(population);
        Individual parent2 = tournament_selection(population);
        Individual child = crossover(parent1, parent2, points);
        mutate(&child);
        new_population[i] = child;
        if (child.fitness < target_distance)
        { // Verifica o critério de parada
            for (int j = 0; j < pop_size; j++)
            {
                population[j] = new_population[j];
            }
            return true;
        }
    }
    for (int i = 0; i < pop_size; i++)
    {
        population[i] = new_population[i];
    }
    return false;

    // todo - agrupar pais e filhos em uma lista ordenada pelo fitness e retornar os N (pop_size) melhores
}

// Encontra o melhor indivíduo na população
Individual find_best_individual(Individual population[])
{
    Individual best_individual = population[0];
    for (int i = 1; i < pop_size; i++)
    {
        // printf("%d FITNESS: %.2f \n", i, population[i].fitness);
        if (population[i].fitness < best_individual.fitness)
        {
            best_individual = population[i];
        }
    }
    return best_individual;
}

// Função para ler coordenadas de um arquivo
void ler_coordenadas(const char *nome_arquivo, Point points[])
{
    FILE *arquivo = fopen(nome_arquivo, "r");
    if (arquivo == NULL)
    {
        printf("Erro ao abrir o arquivo.\n");
        exit(1);
    }
    int id;
    double x, y, z;
    for (int i = 0; i < n; i++)
    {
        fscanf(arquivo, "%lf %lf %lf", &x, &y, &z);
        points[i].id = i;
        points[i].x = x;
        points[i].y = y;
        points[i].z = z;
    }
    for (int i = 0; i < n; i++)
        // {
        //     printf("ID: %d, X: %.6f, Y: %.6f, Z: %.6f\n", points[i].id, points[i].x, points[i].y, points[i].z);
        // }
        fclose(arquivo);
}

// Função para calcular e imprimir a taxa de convergência
double taxa_convergencai(double best_fitness[])
{
    return (best_fitness[iterations - 1] - best_fitness[0]) / best_fitness[0];
}

double ga(const char *nome_arquivo)
{
    srand(time(NULL));
    // Carregar coordenadas do arquivo
    Point points[n];

    ler_coordenadas(nome_arquivo, points);

    // Inicializar a população
    Individual population[pop_size];
    initialize_population(population, points);

    // Array para armazenar o fitness do melhor indivíduo em cada geração
    double best_fitness[iterations];

    // Loop pricipal
    for (int i = 0; i < iterations; i++)
    {
        if (evolve_population(population, points))
        {
            // printf("Parada atingida: caminho menor que %.2f encontrado\n", target_distance);
            break;
        }

        // Encontrar o melhor indivíduo da geração atual
        Individual best_individual = find_best_individual(population);
        best_fitness[i] = best_individual.fitness;

        // if (i % 1000 == 0)
        // {

        //     // printf("Iteracao: %d\n", i);
        //     // printf("Comprimento do melhor caminho: %.2f\n", best_individual.fitness);
        //     // printf("Caminho:\n");
        //     // for (int j = 0; j < n; j++)
        //     // {
        //     //     printf("%d ", best_individual.path[j]);
        //     // }
        //     // printf("\n");
        // }
    }

    // Encontrar o melhor indivíduo
    Individual best_individual = find_best_individual(population);

    // Imprimir o melhor caminho encontrado
    // printf("Melhor caminho encontrado:\n");
    // for (int i = 0; i < n; i++)
    // {
    //     printf("%d ", best_individual.path[i]);
    // }
    // printf("\n");

    // Imprime o caminho
    printf("[");
    for (int i = 0; i < n; i++)
    {
        if (i < n - 1)
        {
            printf("%d, ", best_individual.path[i]);
        }
        else
        {
            printf("%d", best_individual.path[i]);
        }
    }
    printf(", 0]");

    // Imprimir o comprimento do melhor caminho encontrado
    // printf("Comprimento do melhor caminho: %.2f\n", best_individual.fitness);

    // Imprimir a taxa de convergência
    return taxa_convergencai(best_fitness);
}

void gravarLog(char msg[])
{
    FILE *file = fopen("log_ga.txt", "a"); // "a" para abrir em modo append (adicionar no final)
    if (file == NULL)
    {
        perror("Erro ao abrir o arquivo de log");
        return;
    }

    fprintf(file, msg);
    fclose(file);
}

void gerarGrid(int popSizeMin, int popSizeMax, float mutationRateMin, float mutationRateMax)
{
    int best_pop;
    double best_mutation;
    double best_taxa = 100;

    for (int i = popSizeMin; i < popSizeMax; i += 10)
    {
        pop_size = i;
        for (float j = mutationRateMin; j < mutationRateMax; j += 0.01)
        {
            mutation_rate = j;
            double taxa = ga("C:\\Users\\Getaruck\\Documents\\StarToursSolutionSim\\datasets\\star100.xyz.txt");
            char msg[300];
            sprintf(msg, "[popSize:%d, mutationRate:%f] taxa de convergencia = %.6f\n", i, j, taxa);

            gravarLog(msg);

            if (taxa < best_taxa)
            {
                best_taxa = taxa;
                best_pop = i;
                best_mutation = j;
            }
        }
    }

    char msg_best[200];
    sprintf(msg_best, "Melhor combinacao: pop_size = %d , mutation_rate = %f  \nconvergencia = %.6f", best_pop, best_mutation, best_taxa);
    gravarLog(msg_best);
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
    snprintf(nomeArquivo, sizeof(nomeArquivo), "datasets/%s", argv[1]);

    int tamanho = atoi(argv[2]);
    if (tamanho <= 0)
    {
        fprintf(stderr, "Tamanho inválido: %s\n", argv[2]);
        return EXIT_FAILURE;
    }
    n = tamanho;

    const char *str = argv[3];
    char *endptr;
    float mutation_rate_recived;

    mutation_rate_recived = strtof(str, &endptr);
    if (mutation_rate_recived <= 0)
    {
        fprintf(stderr, "mutatio_rate inválido: %s\n", argv[3]);
        return EXIT_FAILURE;
    }
    mutation_rate = mutation_rate_recived;

    int pop_size_recived = atoi(argv[4]);
    if (pop_size_recived <= 0)
    {
        fprintf(stderr, "pop_size_recived inválido: %s\n", argv[4]);
        return EXIT_FAILURE;
    }
    pop_size = pop_size_recived;

    int iterations_recived = atoi(argv[5]);
    if (iterations_recived <= 0)
    {
        fprintf(stderr, "iterations_recived inválido: %s\n", argv[5]);
        return EXIT_FAILURE;
    }
    iterations = iterations_recived;

    ga(nomeArquivo);
    return 0;
}
