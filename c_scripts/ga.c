#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

float mutation_rate = 0.05;
int pop_size = 30;
int iterations = 10000;
int n = 100;
float target_distance = 1700;

typedef struct
{
    int id;
    double x;
    double y;
    double z;
} Point;

typedef struct
{
    int *path;
    double fitness;
} Individual;

FILE *create_log_file()
{
    const char *directory = "c_scripts/logs";

    char filename[100];
    sprintf(filename, "%s/log_ga_%d_%.2f_%d_%d.txt", directory, n, mutation_rate, pop_size, iterations);

    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        perror("Erro ao criar o arquivo");
        return NULL;
    }

    return file;
}

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

float calcularDistancia(Point ponto1, Point ponto2)
{
    float distancia;
    distancia = sqrt(pow(ponto2.x - ponto1.x, 2) + pow(ponto2.y - ponto1.y, 2) + pow(ponto2.z - ponto1.z, 2));
    return distancia;
}

float **criarMatrizDistancias(Point *coordenadas, int tamanho)
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

        for (int j = 0; j <= i; j++)
        {
            if (i == j)
            {
                matrizDistancias[i][j] = 0.0f;
            }
            else
            {
                matrizDistancias[i][j] = calcularDistancia(coordenadas[i], coordenadas[j]);
                matrizDistancias[j][i] = matrizDistancias[i][j];
            }
        }
    }

    return matrizDistancias;
}

void liberarMatrizDistancias(float **matrizDistancias, int tamanho)
{
    for (int i = 0; i < tamanho; i++)
    {
        free(matrizDistancias[i]);
    }
    free(matrizDistancias);
}

double calculate_fitness(Individual individual, float **distances)
{
    double length = 0.0;
    for (int i = 0; i < n - 1; i++)
    {
        length += distances[individual.path[i]][individual.path[i + 1]];
    }
    length += distances[individual.path[n - 1]][individual.path[0]];
    return length;
}

void initialize_population(Individual *population, float **distances)
{
    for (int i = 0; i < pop_size; i++)
    {
        population[i].path = (int *)malloc(n * sizeof(int));
        if (population[i].path == NULL)
        {
            fprintf(stderr, "Erro ao alocar memória para o caminho do indivíduo %d\n", i);
            exit(EXIT_FAILURE);
        }

        for (int j = 0; j < n; j++)
        {
            population[i].path[j] = j;
        }

        for (int j = n - 1; j > 0; j--)
        {
            int k = rand() % (j);

            int temp = population[i].path[j];
            population[i].path[j] = population[i].path[k];
            population[i].path[k] = temp;
        }

        population[i].fitness = calculate_fitness(population[i], distances);
    }
}

void free_population(Individual *population)
{
    for (int i = 0; i < pop_size; i++)
    {
        free(population[i].path);
    }
}


Individual tournament_selection(Individual *population)
{
    Individual parent1 = population[rand() % pop_size];
    Individual parent2 = population[rand() % pop_size];
    return (parent1.fitness < parent2.fitness) ? parent1 : parent2;
}

Individual crossover(Individual parent1, Individual parent2, float **distances)
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
    child.path = (int *)malloc(n * sizeof(int));
    if (!child.path) {
        fprintf(stderr, "Erro ao alocar memória para o caminho no crossover\n");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < n; i++)
    {
        child.path[i] = -1;
    }

    for (int i = start; i <= end; i++)
    {
        child.path[i] = parent1.path[i];
    }

    int index = (end + 1) % n;
    for (int i = 0; i < n; i++)
    {
        int gene = parent2.path[i];

        bool contains = false;
        for (int j = start; j <= end; j++)
        {
            if (child.path[j] == gene)
            {
                contains = true;
                break;
            }
        }

        if (!contains)
        {
            child.path[index] = gene;
            index = (index + 1) % n;
        }
    }

    child.fitness = calculate_fitness(child, distances);

    return child;
}

void mutate(Individual *individual)
{
    if ((double)rand() / RAND_MAX < mutation_rate)
    {
        int start = rand() % (n - 1);
        int end = rand() % (n - 1);
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

int compare_fitness(const void *a, const void *b)
{
    Individual *ind1 = (Individual *)a;
    Individual *ind2 = (Individual *)b;
    return (ind1->fitness > ind2->fitness) - (ind1->fitness < ind2->fitness);
}

bool evolve_population(Individual *population, float **distances)
{
    Individual *combined_population = (Individual *)malloc(2 * pop_size * sizeof(Individual));
    if (!combined_population) {
        fprintf(stderr, "Erro ao alocar memória para a população combinada\n");
        exit(EXIT_FAILURE);
    }

    int index = 0;

    // Copia a população atual para combined_population
    for (int i = 0; i < pop_size; i++)
    {
        combined_population[index++] = population[i];
    }

    // Gera novos filhos e os adiciona à população combinada
    for (int i = 0; i < pop_size; i++)
    {
        Individual parent1 = tournament_selection(population);
        Individual parent2 = tournament_selection(population);
        Individual child = crossover(parent1, parent2, distances);
        mutate(&child);

        combined_population[index++] = child;

        // Se um filho atinge o critério de fitness, encerra a evolução
        if (child.fitness < target_distance)
        {
            qsort(combined_population, index, sizeof(Individual), compare_fitness);

            // Atualiza a população com os melhores indivíduos
            for (int j = 0; j < pop_size; j++)
            {
                population[j] = combined_population[j];
            }

            // Libera memória dos indivíduos não utilizados
            for (int j = pop_size; j < index; j++)
            {
                free(combined_population[j].path);
            }
            free(combined_population);

            return true;
        }
    }

    // Ordena a população combinada por fitness
    qsort(combined_population, index, sizeof(Individual), compare_fitness);

    // Atualiza a população com os melhores indivíduos
    for (int i = 0; i < pop_size; i++)
    {
        population[i] = combined_population[i];
    }

    // Libera memória dos indivíduos não utilizados
    for (int i = pop_size; i < index; i++)
    {
        free(combined_population[i].path);
    }
    free(combined_population);

    return false;
}

Individual find_best_individual(Individual *population)
{
    Individual best_individual = population[0];
    for (int i = 1; i < pop_size; i++)
    {
        if (population[i].fitness < best_individual.fitness)
        {
            best_individual = population[i];
        }
    }
    return best_individual;
}

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
    fclose(arquivo);
}

void ga(const char *nome_arquivo)
{
    clock_t inicio = clock();
    srand(42);
    FILE *log_file = create_log_file();
    Point points[n];

    ler_coordenadas(nome_arquivo, points);

    Individual *population = (Individual *)malloc(pop_size * sizeof(Individual));

    float **distances = criarMatrizDistancias(points, n);
    initialize_population(population, distances);

    double best_fitness[iterations];

    for (int i = 0; i < iterations; i++)
    {
        if (evolve_population(population, distances))
        {
            break;
        }

        Individual best_individual = find_best_individual(population);
        best_fitness[i] = best_individual.fitness;

        clock_t atual = clock();
        double tempo_decorrido = (double)(atual - inicio) / CLOCKS_PER_SEC;
        save_log(log_file, i + 1, best_individual.fitness, tempo_decorrido);
    }

    Individual best_individual = find_best_individual(population);

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
    printf(", %d]", best_individual.path[0]);

    free_population(population);
    free(population);
    liberarMatrizDistancias(distances, n);
}

int main(int argc, char *argv[])
{
    char nomeArquivo[256];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "datasets/%s", argv[1]);

    n = atoi(argv[2]);
    mutation_rate = strtof(argv[3], NULL);
    pop_size = atoi(argv[4]);
    iterations = atoi(argv[5]);

    ga(nomeArquivo);

    return 0;
}