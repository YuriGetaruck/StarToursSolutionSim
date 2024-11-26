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
float target_distance = 1700;

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

FILE *create_log_file()
{
    // Nome do diretório
    const char *directory = "c_scripts/logs";

    // Buffer para o nome do arquivo
    char filename[100];
    sprintf(filename, "%s/log_ga_%d_%.2f_%d_%d.txt", directory, n, mutation_rate, pop_size, iterations);

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
            int k = rand() % (j);

            // Trocar os valores dos índices j e k (exceto para o ponto inicial)
            // if (k != 0) // Não embaralhar o ponto de partida
            // {
                int temp = population[i].path[j];
                population[i].path[j] = population[i].path[k];
                population[i].path[k] = temp;
            // }
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

// Realiza o cruzamento entre dois indivíduos para gerar um novo indivíduo usando Order Crossover (OX)
Individual crossover(Individual parent1, Individual parent2, Point *points)
{
    // Define os pontos de corte aleatoriamente
    int start = rand() % n;
    int end = rand() % n;
    if (start > end)
    {
        int temp = start;
        start = end;
        end = temp;
    }

    Individual child;

    // Inicializa o caminho do filho com -1 (indica posições não preenchidas)
    for (int i = 0; i < n; i++)
    {
        child.path[i] = -1;
    }

    // Copia o segmento do pai 1 para o filho
    for (int i = start; i <= end; i++)
    {
        child.path[i] = parent1.path[i];
    }

    // Preenche o restante com genes do pai 2 na ordem em que aparecem
    int index = (end + 1) % n; // Começa após o final do segmento copiado
    for (int i = 0; i < n; i++)
    {
        int gene = parent2.path[i];

        // Verifica se o gene já está presente no segmento copiado do pai 1
        bool contains = false;
        for (int j = start; j <= end; j++)
        {
            if (child.path[j] == gene)
            {
                contains = true;
                break;
            }
        }

        // Se o gene não estiver presente, adiciona ao filho
        if (!contains)
        {
            child.path[index] = gene;
            index = (index + 1) % n; // Avança circularmente
        }
    }

    // Calcula o fitness do filho
    child.fitness = calculate_fitness(child, points);

    return child;
}


// Realiza mutação em um indivíduo
void mutate(Individual *individual)
{
    if ((double)rand() / RAND_MAX < mutation_rate)
    {
        int start = rand() % (n - 1); // Ignorar o ponto de partida
        int end = rand() % (n - 1);   // Ignorar o ponto de partida
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

// Comparador para ordenar indivíduos por fitness (menor fitness primeiro)
int compare_fitness(const void *a, const void *b)
{
    Individual *ind1 = (Individual *)a;
    Individual *ind2 = (Individual *)b;
    return (ind1->fitness > ind2->fitness) - (ind1->fitness < ind2->fitness);
}

// Evolui a população por uma geração e verifica o critério de parada
bool evolve_population(Individual population[], Point points[])
{
    Individual combined_population[2 * pop_size];
    int index = 0;

    // Copia a população atual para a lista combinada
    for (int i = 0; i < pop_size; i++)
    {
        combined_population[index++] = population[i];
    }

    // Gera nova população (filhos)
    for (int i = 0; i < pop_size; i++)
    {
        Individual parent1 = tournament_selection(population);
        Individual parent2 = tournament_selection(population);
        Individual child = crossover(parent1, parent2, points);
        mutate(&child);

        // Adiciona o filho à lista combinada
        combined_population[index++] = child;

        // Verifica o critério de parada
        if (child.fitness < target_distance)
        {
            // Ordena a população combinada pelo fitness
            qsort(combined_population, index, sizeof(Individual), compare_fitness);

            // Seleciona os melhores para a nova população
            for (int j = 0; j < pop_size; j++)
            {
                population[j] = combined_population[j];
            }
            return true;
        }
    }

    // Ordena a população combinada pelo fitness
    qsort(combined_population, index, sizeof(Individual), compare_fitness);

    // Seleciona os melhores para a nova população
    for (int i = 0; i < pop_size; i++)
    {
        population[i] = combined_population[i];
    }

    return false;
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
    //for (int i = 0; i < n; i++)
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
    clock_t inicio = clock();
    srand(42);
    FILE *log_file = create_log_file();
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

        clock_t autal = clock();
        double tempo_decorrido = (double)(autal - inicio) / CLOCKS_PER_SEC;
        save_log(log_file, i + 1, best_individual.fitness, tempo_decorrido);
    }

    // Encontrar o melhor indivíduo
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
