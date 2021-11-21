from seaborn.matrix import heatmap
from algoritmo_corr_pasillos import *
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from generacion_de_recorridos import *
from heatmap import generar_figura_completa_estacional, heatmap_pasillos_E3
from correlaciones_pasillos import *
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

n_boletas = 1000
# Booleans que sirven para mostrar los heatmaps de cada fase
FASE_0 = False
FASE_1 = False
FASE_2 = False
FASE_CORR = False

'** FASE 0'
supermercado = fase_0()
if FASE_0:
    heatmap = generar_figura_completa_estacional(supermercado, '1')

'** FASE 1'
supermercado = fase_1(supermercado)
if FASE_1:
    heatmap = heatmap_pasillos_E3(supermercado)
    supermercado.distribucion_distancias("Fase 1", n_boletas)
    heatmap = generar_figura_completa_estacional(supermercado, '2')

'** FASE 2'
supermercado = fase_2(supermercado)
if FASE_2:
    heatmap = heatmap_pasillos_E3(supermercado)
    supermercado.distribucion_distancias("Fase 2", n_boletas)
    heatmap = generar_figura_completa_estacional(supermercado, '3')

'** FASE CORRELACIONES'
' La línea de abajo no es necesaria si el archivo ya posee las correlaciones actualizadas ya está escrito.'
#correlaciones_pasillo(supermercado, n_boletas, False)

' ALGORITMO CORRELACIONES'
p_sup_alg, p_inf_alg = algoritmo_correlaciones()
#print("PASILLO SUPERIOR: \n", p_sup_alg)
#print(len(p_sup_alg))
#print("PASILLO INFERIOR: \n", p_inf_alg)
#print(len(p_inf_alg))

' Asignación MANUAL'
# Asignación MANUAL óptima de algoritmo correlaciones_pasillos (hecha por Coloro)
#p_sup, p_inf = ASIGNACION_OPTIMA_CORR_PASILLOS_MANUAL
#pasillo_positioner(supermercado, p_inf, p_sup_alg)

if FASE_CORR:
    #heatmap_correlaciones(correlaciones)
    heatmap = heatmap_pasillos_E3(supermercado)
    distancias = supermercado.distribucion_distancias("post_algoritmo_correlaciones", n_boletas)
    #heatmap = generar_figura_completa_estacional(supermercado, '4')
    pass


if FASE_0 or FASE_1 or FASE_2 or FASE_CORR:
    plt.show()
