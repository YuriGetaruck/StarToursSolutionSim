#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <time.h>

#define N_POINTS 100 // número de pontos no arquivo

// Função para calcular a distância Euclidiana entre dois pontos 3D
double distance(double point1[3], double point2[3])
{
    return sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2) + pow(point1[2] - point2[2], 2));
}

// Função para carregar os pontos a partir de um arquivo .txt
int load_points(const char *filename, double **points)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        printf("Erro ao abrir o arquivo.\n");
        return -1;
    }

    for (int i = 0; i < N_POINTS; i++)
    {
        if (fscanf(file, "%lf %lf %lf", &points[i][0], &points[i][1], &points[i][2]) != 3)
        {
            printf("Erro ao ler os pontos do arquivo.\n");
            fclose(file);
            return -1;
        }
    }

    fclose(file);
    return 0;
}

void ant_colony_optimization(double **points, int n_ants, int n_iterations, double alpha, double beta, double evaporation_rate, double Q)
{
    srand(time(NULL));
    // Alocar dinamicamente a matriz de feromônios
    double **pheromone = (double **)malloc(N_POINTS * sizeof(double *));
    for (int i = 0; i < N_POINTS; i++)
    {
        pheromone[i] = (double *)malloc(N_POINTS * sizeof(double));
    }

    // Alocar dinamicamente a matriz de caminhos
    int **paths = (int **)malloc(n_ants * sizeof(int *));
    for (int i = 0; i < n_ants; i++)
    {
        paths[i] = (int *)malloc(N_POINTS * sizeof(int));
    }

    double *path_lengths = (double *)malloc(n_ants * sizeof(double));
    double best_path_length = DBL_MAX;
    int best_path[N_POINTS];

    // Inicializa a matriz de feromônios
    for (int i = 0; i < N_POINTS; i++)
    {
        for (int j = 0; j < N_POINTS; j++)
        {
            pheromone[i][j] = 1.0;
        }
    }

    for (int iteration = 0; iteration < n_iterations; iteration++)
    {
        // Para cada formiga
        for (int ant = 0; ant < n_ants; ant++)
        {
            int visited[N_POINTS] = {0};
            int current_point = rand() % N_POINTS;
            visited[current_point] = 1;
            paths[ant][0] = current_point;
            double path_length = 0;

            // Constrói o caminho para a formiga
            for (int step = 1; step < N_POINTS; step++)
            {
                int unvisited[N_POINTS];
                int n_unvisited = 0;
                double probabilities[N_POINTS];

                // Encontra pontos não visitados
                for (int i = 0; i < N_POINTS; i++)
                {
                    if (!visited[i])
                    {
                        unvisited[n_unvisited++] = i;
                    }
                }

                double total_prob = 0;
                // Calcula probabilidades
                for (int i = 0; i < n_unvisited; i++)
                {
                    int unvisited_point = unvisited[i];
                    double dist = distance(points[current_point], points[unvisited_point]);
                    probabilities[i] = pow(pheromone[current_point][unvisited_point], alpha) / pow(dist, beta);
                    total_prob += probabilities[i];
                }

                // Normaliza as probabilidades
                for (int i = 0; i < n_unvisited; i++)
                {
                    probabilities[i] /= total_prob;
                }

                // Escolhe o próximo ponto baseado nas probabilidades
                double r = (double)rand() / RAND_MAX;
                double cumulative_prob = 0;
                int next_point = -1;

                for (int i = 0; i < n_unvisited; i++)
                {
                    cumulative_prob += probabilities[i];
                    if (r <= cumulative_prob)
                    {
                        next_point = unvisited[i];
                        break;
                    }
                }

                // Atualiza o caminho e a distância total
                paths[ant][step] = next_point;
                path_length += distance(points[current_point], points[next_point]);
                visited[next_point] = 1;
                current_point = next_point;
            }

            // Fecha o ciclo retornando ao ponto inicial
            path_length += distance(points[paths[ant][N_POINTS - 1]], points[paths[ant][0]]);
            path_lengths[ant] = path_length;

            // Verifica se este é o melhor caminho encontrado
            if (path_length < best_path_length)
            {
                best_path_length = path_length;
                for (int i = 0; i < N_POINTS; i++)
                {
                    best_path[i] = paths[ant][i];
                }
            }
        }

        // Atualiza os feromônios com evaporação
        for (int i = 0; i < N_POINTS; i++)
        {
            for (int j = 0; j < N_POINTS; j++)
            {
                pheromone[i][j] *= evaporation_rate;
            }
        }

        // Adiciona o feromônio com base nos novos caminhos
        for (int ant = 0; ant < n_ants; ant++)
        {
            for (int i = 0; i < N_POINTS - 1; i++)
            {
                pheromone[paths[ant][i]][paths[ant][i + 1]] += Q / path_lengths[ant];
            }
            pheromone[paths[ant][N_POINTS - 1]][paths[ant][0]] += Q / path_lengths[ant];
        }
    }

    // Libera a memória alocada dinamicamente
    for (int i = 0; i < N_POINTS; i++)
    {
        free(pheromone[i]);
    }
    free(pheromone);

    for (int i = 0; i < n_ants; i++)
    {
        free(paths[i]);
    }
    free(paths);
    free(path_lengths);

    // Imprime o melhor caminho encontrado
    printf("Melhor caminho: ");
    for (int i = 0; i < N_POINTS; i++)
    {
        printf("%d ", best_path[i]);
    }
    printf("\nComprimento do melhor caminho: %f\n", best_path_length);
}

int main()
{

    double **points = (double **)malloc(N_POINTS * sizeof(double *));
    for (int i = 0; i < N_POINTS; i++)
    {
        points[i] = (double *)malloc(3 * sizeof(double));
    }
    // Carrega os pontos a partir do arquivo
    if (load_points("..\\datasets\\star100.xyz.txt", points) != 0)
    {
        return 1; // Sai se houver erro ao carregar os pontos
    }

    // Executa a otimização
    ant_colony_optimization(points, 10, 60, 1.0, 1.0, 0.3, 0.3);

    for (int i = 0; i < N_POINTS; i++)
    {
        free(points[i]);
    }
    free(points);

    return 0;
}
