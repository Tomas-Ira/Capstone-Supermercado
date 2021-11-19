from seaborn.matrix import heatmap
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from generacion_de_recorridos import *
from correlaciones_pasillos import *
from heatmap import generar_figura_completa_estacional, heatmap_pasillos_E3


import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

'''
Se lleva a cabo la solución original del problema:
FASE 0 -> FASE 1 -> FASE 2
'''

supermercado = fase_0()

#heatmap = generar_figura_completa_estacional(supermercado, '1')

supermercado = fase_1(supermercado)

#heatmap = generar_figura_completa_estacional(supermercado, '2')

supermercado = fase_2(supermercado)

#heatmap = generar_figura_completa_estacional(supermercado, '3')
#heatmap = heatmap_pasillos_E3(supermercado)
#plt.show()


#heatmap = heatmap_pasillos_E3(supermercado)
#supermercado.distribucion_distancias("Min Distancia", -1)
#print(supermercado.prom_distancia)

#plt.show()


