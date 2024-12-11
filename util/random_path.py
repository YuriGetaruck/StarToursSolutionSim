import numpy as np
import random
import os

def open_dataset(dataset_neme):
    matriz = []
    with open(dataset_neme, 'r') as arquivo:
        linhas = arquivo.readlines()
        for idx, linha in enumerate(linhas):
            valores = linha.split()
            if len(valores) == 3:
                x, y, z = map(float, valores)
                matriz.append([idx, x, y, z])
    return np.array(matriz)

def calcula_distancia_caminho(caminho):
    distancia_caminho = 0.0
    tam = len(caminho)
    
    match tam:
        case 101:
            coordenadas = open_dataset(os.path.join("datasets","star100.xyz.txt"))
        case 1001:
            coordenadas = open_dataset(os.path.join("datasets","star1k.xyz.txt"))
        case 10001:
            coordenadas = open_dataset(os.path.join("datasets","star10k.xyz.txt"))
        case 37860:
            coordenadas = open_dataset(os.path.join("datasets","kj37859.xyz.txt")) 
        case 109400:
            coordenadas = open_dataset(os.path.join("datasets","hyg109399.xyz.txt"))
    
    for i in range(tam - 1):
        x1, y1, z1 = coordenadas[caminho[i]][1], coordenadas[caminho[i]][2], coordenadas[caminho[i]][3]
        x2, y2, z2 = coordenadas[caminho[i+1]][1], coordenadas[caminho[i+1]][2], coordenadas[caminho[i+1]][3]
        distancia = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        distancia_caminho += distancia

    return distancia_caminho

random.seed(42)

caminho_100 = np.arange(100)
random.shuffle(caminho_100)
caminho_100 = np.append(caminho_100, [caminho_100[0]])

print(calcula_distancia_caminho(caminho_100))

caminho_1000 = np.arange(1000)
random.shuffle(caminho_1000)
caminho_1000 = np.append(caminho_1000, [caminho_1000[0]])

print(calcula_distancia_caminho(caminho_1000))

caminho_10000 = np.arange(10000)
random.shuffle(caminho_10000)
caminho_10000 = np.append(caminho_10000, [caminho_10000[0]])

print(calcula_distancia_caminho(caminho_10000))

caminho_37859 = np.arange(37859)
random.shuffle(caminho_37859)
caminho_37859 = np.append(caminho_37859, [caminho_37859[0]])

print(calcula_distancia_caminho(caminho_37859))

caminho_109399 = np.arange(109399)
random.shuffle(caminho_109399)
caminho_109399 = np.append(caminho_109399, [caminho_109399[0]])

print(calcula_distancia_caminho(caminho_109399))


