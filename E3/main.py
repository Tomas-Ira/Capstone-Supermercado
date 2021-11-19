from seaborn.matrix import heatmap
from algoritmo_corr_pasillos import *
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from generacion_de_recorridos import *
from heatmap import generar_figura_completa_estacional, heatmap_pasillos_E3
from correlaciones_pasillos import *

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
heatmap = heatmap_pasillos_E3(supermercado)
supermercado.distribucion_distancias("Fase 1", -1)

#heatmap = generar_figura_completa_estacional(supermercado, '2')

supermercado = fase_2(supermercado)

#heatmap = generar_figura_completa_estacional(supermercado, '3')
#heatmap = heatmap_pasillos_E3(supermercado)
#supermercado.distribucion_distancias("Fase 2", -1)
#plt.show()

#correlaciones = create_correlaciones_list()
#correlaciones = load_correlaciones(supermercado, correlaciones, -1)
#write_correlaciones(supermercado, correlaciones)
#heatmap_correlaciones(correlaciones)

#algoritmo_correlaciones(supermercado)


#heatmap = heatmap_pasillos_E3(supermercado)
#supermercado.distribucion_distancias("post algoritmo correlaciones", -1)
#print(supermercado.prom_distancia)

plt.show()


