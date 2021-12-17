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
from simulador import *

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

from simulador import load_supermercado
from simulador import load_popularities

'''
Se lleva a cabo la solución original del problema:
FASE 0 -> FASE 1 -> FASE 2 -> FASE_CORR
'''

'** LEER DATOS '
simulada = False
path_datos_simulados = "Boletas Simuladas/Boletas Simuladas2.csv"

if simulada:
    ' Usar datos simulados'
    #boletas = leer_datos_simulados(path_datos_simulados)
else:
    ' Usar datos orignales'
    n_boletas = -1
    boletas = generar_muestra(n_boletas, simulada, mensual=False)

# Booleans que sirven para mostrar los heatmaps de cada fase
SHOW = False
FASE_0 = False
FASE_1 = False
FASE_2 = False
FASE_CORR = False
FASE_CORR_ZONAS = True


'** FASE 0'
if FASE_0 or FASE_1 or FASE_2 or FASE_CORR or FASE_CORR_ZONAS:
    supermercado = fase_0()

if FASE_0 and SHOW:
    nombre = "Fase 0"
    #heatmap = generar_figura_completa_estacional(supermercado, '1')
    #heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias(nombre, boletas)
    supermercado.write_datos_demanda(nombre)

'** FASE 1'
if FASE_1 or FASE_2 or FASE_CORR or FASE_CORR_ZONAS:
    supermercado = fase_1(supermercado)

if FASE_1 and SHOW:
    nombre = "Fase 1"
    #heatmap = generar_figura_completa_estacional(supermercado, '2')
    heatmap = heatmap_pasillos_E3(supermercado)
    supermercado.distribucion_distancias(nombre, boletas)
    supermercado.write_datos_demanda(nombre)

'** FASE 2'
if FASE_2 or FASE_CORR or FASE_CORR_ZONAS:    
    supermercado = fase_2(supermercado)
if FASE_2 and SHOW:
    nombre = "Fase 2"
    heatmap = heatmap_pasillos_E3(supermercado)
    supermercado.distribucion_distancias("Fase 2", boletas)
    supermercado.write_datos_demanda("Fase 2")

'** FASE CORRELACIONES PASILLOS'
if FASE_CORR or FASE_CORR_ZONAS:
    correlaciones_pasillo(supermercado, boletas, True)

    ' Asignación Algoritmo '
    p_sup, p_inf = algoritmo_correlaciones()

    ' Asignación MANUAL '
    # Asignación MANUAL óptima de algoritmo correlaciones_pasillos (hecha por Coloro)
    #p_sup, p_inf = ASIGNACION_OPTIMA_CORR_PASILLOS_MANUAL

    ' Cambiamos los pasillos'
    pasillo_positioner(supermercado, p_inf, p_sup)

if FASE_CORR and SHOW:
    #heatmap_correlaciones(correlaciones)
    nombre = "Correlaciones Pasillo"
    heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias(nombre, boletas)
    supermercado.write_datos_demanda(nombre)
    #heatmap = generar_figura_completa_estacional(supermercado, '4')
    pass

'** FASE CORRELACIONES ZONAS'
if FASE_CORR_ZONAS:
    swaps = 5
    correlaciones_sec = correlaciones_secciones(supermercado, boletas, False)
    generar_swaps_secciones(swaps, supermercado, correlaciones_sec, 10000, simulada, path_datos_simulados)

if FASE_CORR_ZONAS and SHOW:
    string = f"Correlaciones Zonas, n={swaps}"
    #heatmap_correlaciones(correlaciones)
    heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias(string, boletas)
    supermercado.write_datos_demanda(string)
    #heatmap = generar_figura_completa_estacional(supermercado, '4')
    pass

'** SIMULACIÓN'
dict_posiciones = load_dict(supermercado)
boletas_simuladas = leer_datos_simulados(path_datos_simulados)
popular = load_popularities(boletas_simuladas)

supermercado = load_supermercado(dict_posiciones, popular)

if not(SHOW):
    string = "SIM CORR ZONAS"
    #heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias(string, boletas)
    supermercado.write_datos_demanda(string)

if FASE_0 or FASE_1 or FASE_2 or FASE_CORR or FASE_CORR_ZONAS:
    #plt.show()
    pass
