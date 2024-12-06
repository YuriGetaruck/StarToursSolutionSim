#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <time.h>

int n_points = 10000;
int n_ants;
int n_iterations;
double alpha;
double beta;
double evaporation_rate;
double Q;

FILE *create_log_file()
{
    const char *directory = "c_scripts/logs";

    char filename[100];
    sprintf(filename, "%s/log_aco_%d_%d_%.2f_%.2f_%.2f_%.2f_%d.txt", directory, n_points, n_ants, alpha, beta, evaporation_rate, Q, n_iterations);

    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        perror("Erro ao criar o arquivo");
        return NULL;
    }

    return file;
}

void save_log(FILE *file, int iteracao, int distancia_total, double tempo_decorrido)
{
    if (file == NULL)
    {
        perror("Arquivo não está aberto");
        return;
    }

    fprintf(file, "%d,%d,%.3f\n", iteracao, distancia_total, tempo_decorrido);
    fflush(file);
}

double distance(double point1[3], double point2[3])
{
    return sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2) + pow(point1[2] - point2[2], 2));
}

int load_points(const char *filename, double **points)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        printf("Erro ao abrir o arquivo.\n");
        return -1;
    }

    rewind(file);

    for (int i = 0; i < n_points; i++)
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

void ant_colony_optimization(double **points, int n_ants, int n_iterations, double alpha, double beta, double evaporation_rate, double Q, FILE *log_file)
{
    clock_t inicio = clock();
    srand(42);

    double **pheromone = (double **)malloc(n_points * sizeof(double *));
    for (int i = 0; i < n_points; i++)
    {
        pheromone[i] = (double *)malloc(n_points * sizeof(double));
    }

    int **paths = (int **)malloc(n_ants * sizeof(int *));
    for (int i = 0; i < n_ants; i++)
    {
        paths[i] = (int *)malloc((n_points + 1) * sizeof(int));
    }

    double *path_lengths = (double *)malloc(n_ants * sizeof(double));
    double best_path_length = DBL_MAX;
    int best_path[n_points];

    for (int i = 0; i < n_points; i++)
    {
        for (int j = 0; j < n_points; j++)
        {
            pheromone[i][j] = 1.0;
        }
    }

    for (int iteration = 0; iteration < n_iterations; iteration++)
    {
        for (int ant = 0; ant < n_ants; ant++)
        {
            int visited[n_points + 1];
            memset(visited, 0, sizeof(visited));

            int current_point = ant % n_points;

            visited[current_point] = 1;
            paths[ant][0] = current_point;
            double path_length = 0;

            for (int step = 1; step < n_points; step++)
            {
                int unvisited[n_points];
                int n_unvisited = 0;
                double probabilities[n_points];

                for (int i = 0; i < n_points; i++)
                {
                    if (!visited[i])
                    {
                        unvisited[n_unvisited++] = i;
                    }
                }

                double total_prob = 0;
                for (int i = 0; i < n_unvisited; i++)
                {
                    int unvisited_point = unvisited[i];
                    double dist = distance(points[current_point], points[unvisited_point]);
                    probabilities[i] = pow(pheromone[current_point][unvisited_point], alpha) / pow(dist, beta);
                    total_prob += probabilities[i];
                }

                for (int i = 0; i < n_unvisited; i++)
                {
                    probabilities[i] /= total_prob;
                }

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

                if (next_point == -1)
                {
                    next_point = unvisited[n_unvisited - 1];
                }

                paths[ant][step] = next_point;
                path_length += distance(points[current_point], points[next_point]);
                visited[next_point] = 1;
                current_point = next_point;
            }

            for (int i = 0; i < n_points; i++)
            {
                if (!visited[i])
                {
                    printf("Erro: O ponto %d não foi visitado.\n", i);
                }
            }

            path_length += distance(points[current_point], points[0]);
            path_lengths[ant] = path_length;

            if (path_length < best_path_length)
            {
                best_path_length = path_length;
                for (int i = 0; i < n_points; i++)
                {
                    best_path[i] = paths[ant][i];
                }
            }
        }

        for (int i = 0; i < n_points; i++)
        {
            for (int j = 0; j < n_points; j++)
            {
                pheromone[i][j] *= evaporation_rate;
            }
        }

        for (int ant = 0; ant < n_ants; ant++)
        {
            for (int i = 0; i < n_points - 1; i++)
            {
                pheromone[paths[ant][i]][paths[ant][i + 1]] += Q / path_lengths[ant];
            }
            pheromone[paths[ant][n_points - 1]][paths[ant][0]] += Q / path_lengths[ant];
        }
        
        clock_t autal = clock();
        double tempo_decorrido = (double)(autal - inicio) / CLOCKS_PER_SEC;

        save_log(log_file, iteration + 1, best_path_length, tempo_decorrido);
    }

    for (int i = 0; i < n_points; i++)
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

    printf("[");
    for (int i = 0; i < n_points; i++)
    {
        printf("%d, ", best_path[i]);
    }
    printf("%d]", best_path[0]);
}

int main(int argc, char *argv[])
{
    char nomeArquivo[50];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "datasets/%s", argv[1]);

    n_points = atoi(argv[2]);
    n_ants = atoi(argv[3]);
    n_iterations = atoi(argv[4]);
    const char *str_alpha = argv[5];
    char *endptr_alpha;
    alpha = strtof(str_alpha, &endptr_alpha);
    const char *str_beta = argv[6];
    char *endptr_beta;
    beta = strtof(str_beta, &endptr_beta);
    const char *str_eva = argv[7];
    char *endptr_eva;
    evaporation_rate = strtof(str_eva, &endptr_eva);
    const char *str_q = argv[8];
    char *endptr_q;
    Q = strtof(str_q, &endptr_q);

    FILE *log_file = create_log_file();

    double **points = (double **)malloc(n_points * sizeof(double *));
    for (int i = 0; i < n_points; i++)
    {
        points[i] = (double *)malloc(3 * sizeof(double));
    }
    if (load_points(nomeArquivo, points) != 0)
    {
        return 1;
    }

    ant_colony_optimization(points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q, log_file);

    for (int i = 0; i < n_points; i++)
    {
        free(points[i]);
    }
    free(points);

    return 0;
}
