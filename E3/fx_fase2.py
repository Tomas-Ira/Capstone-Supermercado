from data_work import ordenados
from model import *
from heatmap import generar_figura_completa_estacional

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

def asignar_zona_uniforme(pasillos, zona):
    '''
    Esta funcion se encarga de a que pasillo se debe asignar la siguiente zona y se lo asigna
    
    INPUT:
    * pasillos -> Lista de instancias de Pasillos()
    
    OUTPUT:
    * None
    '''
    posicion = -1
    min = 1000000
    #Comenzamos revisando que pasillo que aún tiene capacidad para zonas tiene la menor demanda
    for i in range(len(pasillos)):
        pasillo = pasillos[i]
        #Primeros 15 tienen capacidad para 8 zonas
        if i < 15:
            if len(pasillo.zonas) < 8:
                if pasillo.demanda < min:
                    min = pasillo.demanda
                    posicion = i
        #Los pasillos inferiores tienen capacidad para 9 zonas
        else:
            if len(pasillo.zonas) < 9:
                if pasillo.demanda < min:
                    min = pasillo.demanda
                    posicion = i

    #Agrego la zona
    if posicion >= 0:
        pasillo = pasillos[posicion]
        pasillo.zonas.append(zona)
        pasillo.calcular_demanda()

def fase_2(super):
    '''
    Esta funcion se encarga de asignar las zonas ya homogenizadas en la fase 1 a los pasillos del supermercado,
    con el objetivo de lograr que sea lo más pareja posible.
    Corresponde a la FASE 2 planteada para la solución del problema.
    
    INPUT:
    * super -> class Supermercado()
    
    OUTPUT:
    * Objeto Supermercado() con pasillos y zonas homogeneas
    '''
    
    #Obtenemos una lista ordenada de las zonas (de mayor a menor)
    zonas = []
    for pasillo in super.pasillos:
        for zona in pasillo.zonas:
            zonas.append(zona)
    zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda, reverse=True)
    
    #Creamos un listado con 27 pasillos (15 superiores + 12 inferiores)
    pasillos = [Pasillo(x+1) for x in range(27)]
    
    #Asignamos un primer producto a cada pasillo
    for i in range(27):
        pasillos[i].zonas.append(zonas_ordenadas[i])
        pasillos[i].calcular_demanda()

    #Asignamos cada zona al pasillo que le corresponde según el algoritmo
    for i in range(27, 228):
        asignar_zona_uniforme(pasillos, zonas_ordenadas[i])

    #Agregamos zonas de pasillos inferiores a pasillos superiores (por consistencia con el modelo Supermercado)
    for i in range(12):
        pasillo_original = pasillos[i]
        pasillo_desechable = pasillos[i+15]
        for z in pasillo_desechable.zonas:
            pasillo_original.zonas.append(z)

    super.pasillos = pasillos[:15]
    #Finaliza asignacion a pasillos

    # Calculamos distancia recorrida, se imprimen en el archivo 'distancias_recorridas.txt'
    nro_boletas_muestra = 1000   # -1 es todas.
    archivo_distancias = 'distancias_recorridas.txt'
    boletas = generar_muestra(nro_boletas_muestra)
    dict_dist_f1, distancias_f1 = calcular_distancia(super, "fase 2", boletas, nombre_archivo=archivo_distancias)
    
    for pasillo in super.pasillos:
        for z in range(len(pasillo.zonas)):
            zona = pasillo.zonas[z]
            zona.id = z + 1

    return super