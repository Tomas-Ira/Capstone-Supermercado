from data_work import ordenados
from model import *
from heatmap import generar_figura_completa_estacional, generar_figura_completa_estacional_stdev, grafico_evolucion_varianza, grafico_evolucion_distancia

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv
import sys

def fase_0():
    '''
    Esta funcion se encarga de generar una primera asignación naive de productos a las zonas.
    Corresponde a la FASE 0 planteada para la solución del problema.
    
    INPUT:
    * None
    
    OUTPUT:
    * Objeto Supermercado() con productos cargados
    '''
    
    '''Abrimos archivo con productos permanentes'''
    
    #filename = "Data/Productos Permanentes.csv"
    filename = f"{sys.path[0]}/Data/Productos Permanentes.csv"
    fields = []
    rows = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row[0])
            
    rows = rows[:-6]
    permanentes_set = set(rows)
    ordenados_permanentes = []
    for producto in ordenados:
        if producto[0] in permanentes_set:
            ordenados_permanentes.append(producto)
    
    #Ordenados permanentes tiene los productos no estacionales con los que se trabajara.
    
    '''Instanciamos el Supermercado y asignamos los productos a cada una de las zonas'''
    
    super = Supermercado()
    super.poblar_fase_0_permanente(ordenados_permanentes)
    
    # Calculamos distancia recorrida, se imprimen en el archivo 'distancias_recorridas.txt'
    nro_boletas_muestra = 1000   # -1 es todas.
    ## Borramos el archivo anterior
    archivo_distancias = 'distancias_recorridas.txt'
    with open(archivo_distancias, 'w') as f:
        f.write("DISTANCIAS RECORRIDAS\n")

    dict_dist_f0, distancias_f0 = calcular_distancia(super, "fase 0", nombre_archivo=archivo_distancias, n=nro_boletas_muestra)
    
    #fig = generar_figura_completa_estacional(super, 'Problema Supermercado - Fase 0')
    #plt.show()
    return super