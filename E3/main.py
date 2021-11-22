from seaborn.matrix import heatmap
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from generacion_de_recorridos import *
from heatmap import generar_figura_completa_estacional, heatmap_pasillos_E3
from correlaciones_pasillos import *
from algoritmo_corr_pasillos import *
from correlaciones_secciones import *
from algoritmo_corr_secciones import *
from constantes import *

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

'''
Se lleva a cabo la solución original del problema:
FASE 0 -> FASE 1 -> FASE 2 -> FASE_CORR
'''

n_boletas = -1
# Booleans que sirven para mostrar los heatmaps de cada fase
FASE_0 = True
FASE_1 = False
FASE_2 = False
FASE_CORR = False
FASE_CORR_ZONAS = False


'** FASE 0'
if FASE_0 or FASE_1 or FASE_2 or FASE_CORR or FASE_CORR_ZONAS:
    supermercado = fase_0()

if FASE_0:
    nombre = "Fase 0"
    #heatmap = generar_figura_completa_estacional(supermercado, '1')
    heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias(nombre, n_boletas)
    supermercado.write_datos_demanda(nombre)

'** FASE 1'
if FASE_1 or FASE_2 or FASE_CORR or FASE_CORR_ZONAS:
    supermercado = fase_1()

if FASE_1:
    nombre = "Fase 1"
    #heatmap = generar_figura_completa_estacional(supermercado, '2')
    heatmap = heatmap_pasillos_E3(supermercado)
    supermercado.distribucion_distancias(nombre, n_boletas)
    supermercado.write_datos_demanda(nombre)

'** FASE 2'
if FASE_2 or FASE_CORR or FASE_CORR_ZONAS:    
    supermercado = fase_2(supermercado)
if FASE_2:
    nombre = "Fase 2"
    heatmap = heatmap_pasillos_E3(supermercado)
    supermercado.distribucion_distancias("Fase 2", n_boletas)
    supermercado.write_datos_demanda("Fase 2")

'** FASE CORRELACIONES PASILLOS'
if FASE_CORR or FASE_CORR_ZONAS:
    correlaciones_pasillo(supermercado, n_boletas, True)

    ' Asignación Algoritmo '
    p_sup, p_inf = algoritmo_correlaciones()

    ' Asignación MANUAL '
    # Asignación MANUAL óptima de algoritmo correlaciones_pasillos (hecha por Coloro)
    #p_sup, p_inf = ASIGNACION_OPTIMA_CORR_PASILLOS_MANUAL

    ' Cambiamos los pasillos'
    pasillo_positioner(supermercado, p_inf, p_sup)

if FASE_CORR:
    #heatmap_correlaciones(correlaciones)
    nombre = "Correlaciones Pasillo"
    heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias(nombre, n_boletas)
    supermercado.write_datos_demanda(nombre)
    #heatmap = generar_figura_completa_estacional(supermercado, '4')
    pass


'** FASE CORRELACIONES ZONAS'
if FASE_CORR_ZONAS:
    swaps = 157
    correlaciones_sec = correlaciones_secciones(supermercado, n_boletas, False)
    generar_swaps_secciones(swaps, supermercado, correlaciones_sec)

if FASE_CORR_ZONAS:
    string = f"Correlaciones Zonas, n={swaps}"
    #heatmap_correlaciones(correlaciones)
    heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias(string, n_boletas)
    supermercado.write_datos_demanda(string)
    #heatmap = generar_figura_completa_estacional(supermercado, '4')
    pass

if FASE_0 or FASE_1 or FASE_2 or FASE_CORR or FASE_CORR_ZONAS:
    plt.show()
