from seaborn.matrix import heatmap
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from heatmap import generar_figura_completa_estacional, heatmap_pasillos_E3
from fx_swap_pasillos import *

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
plt.show()
swap_pasillos(supermercado, 'A1', 'B2')
#heatmap = heatmap_pasillos_E3(supermercado)
#plt.show()


