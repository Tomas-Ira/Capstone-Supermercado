from data_work import ordenados
from model import *
from heatmap import generar_figura_completa_estacional_optima

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

filename = "Problema 2/Productos Permanentes.csv"
fields = []
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row[0])

rows = rows[:-6]
permanentes_set = set(rows)
ordenados_permanentes = []
for producto in ordenados:
    if producto[0] in permanentes_set:
        ordenados_permanentes.append(producto)

#Ordenados permanentes tiene los productos no estacionales con los que se trabajara.


super = Supermercado()
super.poblar_fase_0_permanente(ordenados_permanentes)
"""
# Calculamos distancia recorrida, se imprimen en el archivo 'distancias_recorridas.txt'
## Borramos el archivo anterior
archivo_distancias = 'distancias_recorridas.txt'
with open(archivo_distancias, 'w') as f:
    f.write("DISTANCIAS RECORRIDAS\n")

dict_dist_f0 = calcular_distancia(super, "fase 0", nombre_archivo=archivo_distancias)
"""

#Generamos heatmaps
dda_total = super.calcular_demanda()
demanda_por_seccion = dda_total // 228

for p in super.pasillos:
    for z in p.zonas:
        z.demanda = demanda_por_seccion

fig = generar_figura_completa_estacional_optima(super, 'Distribución uniforme óptima', demanda_por_seccion)
plt.show()