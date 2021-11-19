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

n_boletas = -1

supermercado = fase_0()

#heatmap = generar_figura_completa_estacional(supermercado, '1')
supermercado = fase_1(supermercado)
#heatmap = heatmap_pasillos_E3(supermercado)
#supermercado.distribucion_distancias("Fase 1", n_boletas)

#heatmap = generar_figura_completa_estacional(supermercado, '2')

supermercado = fase_2(supermercado)

#heatmap = generar_figura_completa_estacional(supermercado, '3')
heatmap = heatmap_pasillos_E3(supermercado)
supermercado.distribucion_distancias("Fase 2", n_boletas)
#plt.show()

#correlaciones = create_correlaciones_list()
#correlaciones = load_correlaciones(supermercado, correlaciones, n_boletas)
#write_correlaciones(supermercado, correlaciones)
#heatmap_correlaciones(correlaciones)

#p_sup, p_inf = [['P8A', 'P11A', 'P9A', 'P13A', 'P3A', 'P5A', 'P1A', 'P2A', 'P4A', 'P6A', 'P7A', 'P15A', 'P10A', 'P14A', 'P12A'],
#['P11B', 'P2B', 'P7B', 'P1B', 'P9B', 'P4B', 'P12B', 'P8B', 'P5B', 'P10B', 'P6B', 'P3B', 'P13B', 'P14B', 'P15B']]

#pasillo_positioner(supermercado, p_inf, p_sup)

#for pasillo in supermercado.pasillos:
#    pasillo.demanda

#heatmap = heatmap_pasillos_E3(supermercado)
#supermercado.distribucion_distancias("post algoritmo correlaciones", n_boletas)
print("Promedio:", supermercado.prom_distancia)
print("Moda:", supermercado.moda)
print("Mediana:", supermercado.mediana)
print("Curtosis:", supermercado.curtosis)
print("Desv.", supermercado.desv)

plt.show()


