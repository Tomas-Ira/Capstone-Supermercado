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

def load_correlaciones(correlaciones):
    '''
    Recorre todas las boletas y genera correlaciones entre pasillos, cargándolas en la lista 'correlaciones' de input, que debe 
    ser previamente creada con la función 'create_correlaciones_list'.
    
    * Retorna la lista de correlaciones entre pasillos cargada con datos.
    '''
    boletas = generar_muestra(-1) # -1 implica todas las boletas.
    print('Numero de boletas:', len(boletas))
    primero = True
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
        if contador in [22041, 44082, 66123]:
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

def correlaciones_printer(correlaciones):
    '''
    TODO Imprime la lista de correlaciones ORDENADA en un archivo .txt llamado 'correlaciones_pasillos.txt'.
    '''
    print("Comenzando Sort\n")
    print(np.sort(correlaciones))
    return

correlaciones = create_correlaciones_list()
correlaciones = load_correlaciones(correlaciones)
heatmap_correlaciones(correlaciones)
