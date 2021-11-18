from data_work import ordenados
from model import *
from heatmap import generar_figura_completa_estacional

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

def fase_1(super):
    '''
    Esta funcion se encarga de hacer los swaps necesarios para homogenizar las zonas.
    Corresponde a la FASE 1 planteada para la solución del problema.
    
    INPUT:
    * super -> class Supermercado()
    
    OUTPUT:
    * Objeto Supermercado() con zonas homogeneas
    '''
    #Creamos una lista con todas las zonas
    zonas = []
    for pasillo in super.pasillos:
        for zona in pasillo.zonas:
            zonas.append(zona)
    
    #Comienza el algoritmo iterativo de swaps
    iteracion = 0
    while iteracion < 10:

        #Ordenamos las zonas demenor a mayor demanda
        zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda)
        #Se forman parejas de zonas bajo el criterio:
        # 1ª zona de menor demanda - 1ª zona de mayor demanda
        # 2ª zona de menor demanda - 2ª zona de mayor demanda
        # ...
        #Para cada pareja se utiliza la funcion emparejar_zonas, que realiza los swaps mismos
        for i in range(114):
            emparejar_zonas(zonas_ordenadas[i], zonas_ordenadas[227-i])
        #Termina Algoritmo de swaps Fase 1
        iteracion += 1
        
    # Calculamos distancia recorrida, se imprimen en el archivo 'distancias_recorridas.txt'
    nro_boletas_muestra = 1000   # -1 es todas.
    archivo_distancias = 'distancias_recorridas.txt'
    boletas = generar_muestra(nro_boletas_muestra)
    dict_dist_iter, distancias_iter = calcular_distancia(super, "fase 1", boletas, nombre_archivo=archivo_distancias)
    
    return super

def emparejar_zonas(zona1, zona2):
    '''
    Esta función recibe dos zonas y se encarga de realizar el algoritmo de swaps.
    Como cada zona es un objeto, se hacen los swaps y cada objeto cambia, por lo que 
    no es necesario hacer return de las zonas.
    
    INPUT:
    * zona1 -> class Zona()
    * zona2 -> class Zona()
    
    Output:
    * None
    '''
    
    #Primero obtenemos todos los productos de las zonas y los ordenamos de mayor a menor
    productos = []
    for p in zona1.productos:
        productos.append(p)
    for p in zona2.productos:
        productos.append(p)

    productos = sorted(productos, key=lambda x: int(x[1]), reverse=True)

    productos_1 = []
    productos_2 = []
    
    demanda_1 = 0
    demanda_2 = 0

    n_1 = 0
    n_2 = 0
    
    #Asignamos según algoritmo pre-definido

    for p in productos:
        if n_1 == 50:
            productos_2.append(p)
        elif n_2 == 50:
            productos_1.append(p)
        else:
            if demanda_2 >= demanda_1:
                n_1 += 1
                demanda_1 += int(p[1])
                productos_1.append(p)
            else:
                n_2 += 1
                demanda_2 += int(p[1])
                productos_2.append(p)
    
    zona1.productos = productos_1
    zona2.productos = productos_2
    zona1.calcular_demanda()
    zona2.calcular_demanda()
    