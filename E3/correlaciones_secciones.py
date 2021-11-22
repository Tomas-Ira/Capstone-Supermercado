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
    #print('Numero de boletas:', len(boletas))
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
        '''
        contador += 1
        if n == -1:
            n = 88162
        quarter = n/4
        half = n/2
        third_quarter = 3*n/4
        if contador in [int(quarter), int(half), int(third_quarter)]:
            print('Llevamos:', contador)
        '''
    return correlaciones

def write_correlaciones(supermercado, correlaciones):
    '''
    Imprime la lista de correlaciones ORDENADA en un archivo .txt llamado 'correlaciones_secciones.txt'.
    '''
    # Se ignorará correlaciones entre pasillos inferiores o superiores, esto es opcional, y se puede cambiar
    # cambiando el valor de 'mezclar_pasillos'. Es decir, si 'mezclar_pasillos' es false, se guarda las correlaciones en 
    # dos archivos distintos.
    # OJO no cambiar esto, no esta implementado el caso False
    mezclar_pasillos = True
    # Para el caso de que se quiera todo en un archivo ('mezclar pasillos = True')
    correlaciones_con_nombre = []
    path = "Archivos Correlaciones/correlaciones_secciones.csv"
    # Para el caso de que se quieran las correlaciones superiores e inferiores separadas('mezclar secciones = False')
    correlaciones_con_nombre_superior = []
    correlaciones_con_nombre_inferior = []
    path_superior = "Archivos Correlaciones/correlaciones_secciones_sup.csv"
    path_inferior = "Archivos Correlaciones/correlaciones_secciones_inf.csv"
        
    correlaciones_finales = []
    for i in range(len(correlaciones)):
        for j in range(len(correlaciones[i])):
            if j > i:
                posicion_i = obtener_posicion_seccion(i)
                posicion_j = obtener_posicion_seccion(j)
                
                correlaciones_finales.append([posicion_i, posicion_j, correlaciones[i][j]])
    # Finalmente, imprimimos en el archivo.
    if mezclar_pasillos:
        with open(path, "w") as file:
            correlaciones_finales = sorted(correlaciones_finales, key=lambda x: x[2], reverse=True)
            for tupla in correlaciones_finales:
                string = f"{tupla[0]},{tupla[1]},{tupla[2]}\n"
                file.write(string)
    else:
        # Imprimimos superior
        with open(path_superior, "w") as file:
            for tupla in correlaciones_finales:
                string = f"{tupla[0]},{tupla[1]},{tupla[2]}\n"
                file.write(string)
        # Imprimimos inferior
        with open(path_inferior, "w") as file:
            for tupla in correlaciones_finales:
                string = f"{tupla[0]},{tupla[1]},{tupla[2]}\n"
                file.write(string)
    return

def obtener_posicion_seccion(num):
    pasillo = (num // 17) + 1
    if pasillo > 12:
        seccion = num - (12 * 17)
        pasillo = 13 + (seccion // 8)
    if pasillo < 13:
        seccion = num - (17 * (pasillo - 1)) + 1
    else:
        seccion = num - (12 * 17) - ((pasillo - 13) * 8) + 1
    if seccion <= 8:
        letra = 'A'
    else:
        letra = 'B'
    return 'P' + str(pasillo) + letra + '-' + str(seccion)
        

supermercado = fase_0()
supermercado = fase_1(supermercado)
supermercado = fase_2(supermercado)

correlaciones = create_correlaciones_matrix()
correlaciones = load_correlaciones(supermercado, correlaciones, n=1000)
#write_correlaciones(supermercado, correlaciones)

'''
for i in range(len(correlaciones)):
    if i < 10:
        print(i+1, correlaciones[i])
'''

