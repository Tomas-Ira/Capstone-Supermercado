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

def create_correlaciones_matrix():
    '''
    Crea una matriz de 228 x 228 para poblar con las correlaciones entre secciones.
    
    - Pasillos full: 12 x 17 = 204
    - Pasillos estacionales: 3 x 8 = 24
    - total de secciones = 228
    '''
    correlaciones = []
    for i in range(228):
        correlaciones.append([])
    for i in range(228):
        for j in range(228):
            correlaciones[i].append(0)
    return correlaciones

def load_correlaciones(supermercado, correlaciones, n=-1):
    '''
    Recorre todas las boletas y genera correlaciones entre secciones, cargándolas en la matriz 'correlaciones' de input, que debe 
    ser previamente creada con la función 'create_correlaciones_matrix'.

    INPUT
    * n: cantidad de boletas en muestra, por defecto -1, que significa todas.
    
    * Retorna la matriz de correlaciones entre secciones cargada con datos.
    '''
    boletas = generar_muestra(n) # -1 implica todas las boletas.
    print('Numero de boletas:', len(boletas))
    contador = 0
    for boleta in boletas:
        visitas = contador_visitas_por_seccion(supermercado, boleta)
        #for i in range(len(visitas)):
            #print(i+1, visitas[i])
        visitas_lista = []
        for lista in visitas:
            visitas_lista += lista
        for i in range(228):
            seccion_1 = visitas_lista[i]
            if seccion_1 == 1:
                for j in range(228):
                    seccion_2 = visitas_lista[j]
                    if seccion_2 == 1 and i != j:
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

supermercado = fase_0()
supermercado = fase_1(supermercado)
supermercado = fase_2(supermercado)

correlaciones = create_correlaciones_matrix()
correlaciones = load_correlaciones(supermercado, correlaciones, n=1000)

for i in range(len(correlaciones)):
        print(i+1, correlaciones[i])
