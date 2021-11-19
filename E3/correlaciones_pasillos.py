import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
from Reader import generar_muestra, datos_todos
from model import *
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from random import sample, seed

supermercado = fase_0()
supermercado = fase_1(supermercado)
supermercado = fase_2(supermercado)

DICT_PASILLOS_INDICES = {"P1A": 0, 'P2A': 1,'P3A': 2, 'P4A': 3,'P5A': 4,'P6A': 5,'P7A': 6,'P8A': 7,'P9A': 8,'P10A': 9,'P11A': 10,'P12A': 11,
                'P13A': 12,'P14A': 13, 'P15A': 14, 'P1B': 15, 'P2B': 16,'P3B': 17, 'P4B': 18,'P5B': 19,'P6B': 20,'P7B': 21,'P8B': 22,'P9B': 23,
                'P10B': 24,'P11B': 25,'P12B': 26, 'P13B': 27,'P14B': 28, 'P15B': 29}

DICT_INDICES_PASILLOS = {0: "P1A", 1: 'P2A', 2: 'P3A', 3: 'P4A', 4: 'P5A', 5: 'P6A', 6: 'P7A', 7: 'P8A', 8: 'P9A', 
9: 'P10A', 10: 'P11A', 11: 'P12A', 12: 'P13A', 13: 'P14A', 14: 'P15A', 15: 'P1B', 16: 'P2B', 17: 'P3B', 18: 'P4B',
19: 'P5B', 20: 'P6B', 21: 'P7B', 22: 'P8B', 23: 'P9B', 24: 'P10B', 25: 'P11B', 26: 'P12B', 27: 'P13B', 28: 'P14B',
29: 'P15B'}


def create_correlaciones_list():
    '''
    Crea una lista de lista para cargar las correlaciones.
    La lista que se retorna tiene la siguiente estructura:

      * Posee 27 sub-listas, cada una representando a un pasillo a un pasillo i.
      * Cada sub-lista posee 27 números, correspondiente a las correlaciones del pasillo i con el pasillo en la posición j.
    '''
    correlaciones = []
    for i in range(27):
        correlaciones.append([])
    for i in range(27):
        for j in range(27):
            correlaciones[i].append(0)
    return correlaciones

def load_correlaciones(correlaciones, n=-1):
    '''
    Recorre todas las boletas y genera correlaciones entre pasillos, cargándolas en la lista 'correlaciones' de input, que debe 
    ser previamente creada con la función 'create_correlaciones_list'.

    INPUT
    * n: cantidad de boletas en muestra, por defecto -1, que significa todas.
    
    * Retorna la matriz de correlaciones entre pasillos cargada con datos.
    '''
    boletas = generar_muestra(n) # -1 implica todas las boletas.
    print('Numero de boletas:', len(boletas))
    contador = 0
    for boleta in boletas:
        visitas = contador_visitas_por_pasillo(supermercado, [boleta])
        visitas = visitas[0] + visitas[1]
        for i in range(27):
            pasillo_1 = visitas[i]
            if pasillo_1 == 1:
                for j in range(27):
                    pasillo_2 = visitas[j]
                    if pasillo_1 == 1 and pasillo_2 == 1:
                        correlaciones[i][j] += 1
        contador += 1
        if n == -1:
            n = 88162
        quarter = n/4
        half = n/2
        third_quarter = 3*n/4
        if contador in [int(quarter), int(half), int(third_quarter)]:
            print('Llevamos:', contador)
    return correlaciones
    
def heatmap_correlaciones(correlaciones):
    '''
    Imprime un heatmap de las correlaciones entre pasillos.
    '''
    indices = []
    for i in range(1,16):
        indices.append('P' + str(i) + 'A')
    for i in range(1,13):
        indices.append('P' + str(i) + 'B')

    df = pd.DataFrame(np.array(correlaciones), 
                    columns = indices,
                    index=indices)

    color = sns.color_palette("rocket_r", as_cmap=True)
    heat_map = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap=color)
    plt.show()

def write_correlaciones(correlaciones):
    '''
    Imprime la lista de correlaciones ORDENADA en un archivo .txt llamado 'correlaciones_pasillos.txt'.
    '''
    path = "Archivos Correlaciones/correlaciones_pasillos.csv"
    correlaciones_con_nombre = []

    # Primero creamos una lista con tuplas ('pasillo_1', 'pasillo_2', correlacion_1_2). EJ:  
    for i in range(0, 27):
        for j in range(0, 27):
            if DICT_INDICES_PASILLOS[i] != DICT_INDICES_PASILLOS[j]:
                #tupla = (DICT_INDICES_PASILLOS[i], DICT_INDICES_PASILLOS[j], correlaciones[i][j])
                tupla = (i, j, correlaciones[i][j])
                correlaciones_con_nombre.append(tupla)

    # Ahora, agregamos las demandas propias de cada pasillo.
    demandas = supermercado.heatmap_pasillos()
    for i in range(0, 15):
        # Pasillo A
        tupla = ("E", DICT_INDICES_PASILLOS[i], demandas[0][i])
        correlaciones_con_nombre.append(tupla)
        # Pasillo B
        if i < 12:
            tupla = ("E", DICT_INDICES_PASILLOS[i + 15], demandas[1][i])
            correlaciones_con_nombre.append(tupla)

    # Ahora, sorteamos según correlación.
    correlaciones_con_nombre_ordenada = sorted(correlaciones_con_nombre, key=lambda tupla: tupla[2], reverse=True)

    # Finalmente, imprimimos en el archivo.
    with open(path, "w") as file:
        for tupla in correlaciones_con_nombre_ordenada:
            string = f"{tupla[0]}, {tupla[1]}, {tupla[2]}\n"
            file.write(string)
    return correlaciones_con_nombre_ordenada

correlaciones = create_correlaciones_list()
correlaciones = load_correlaciones(correlaciones, -1)
heatmap_correlaciones(correlaciones)
write_correlaciones(correlaciones)
