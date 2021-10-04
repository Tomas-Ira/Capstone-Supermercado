from data_work import ordenados
from model import *

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat

def emparejar_zonas(zona1, zona2):
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

super = Supermercado()
super.poblar_fase_0(ordenados)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))
fig.suptitle('Problema Supermercado - Fase 0 vs Iteracion 10', fontsize=18)
ax1.set_title("Heatmap Fase 0")
ax2.set_title("Heatmap Iteracion 10")

distribucion_demandas = super.generar_heatmap()
min_5, max_5 = top_5(distribucion_demandas)
guardar_distribucion(super, min_5, max_5, "fase_0.txt")
index_list = max_5 + [0,0,0,0,0] + min_5
df = pd.DataFrame(np.array(distribucion_demandas), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=[str(x) for x in range(1,18)])

labels = df.applymap(lambda v: str(5 - (index_list.index(v)%10)) if v in index_list else '')

heat_map_1 = sns.heatmap(df, robust=True, linewidths=0.05, annot=labels, annot_kws={'fontsize':12}, fmt='', cmap="rocket_r", ax=ax1)

iteracion = 0
text_1 = "Desviacion estandar iteracion "
zonas = []
for pasillo in super.pasillos:
    for zona in pasillo.zonas:
        zonas.append(zona)

demandas_productos = []
for z in zonas:
    for p in z.productos:
        demandas_productos.append(int(p[1]))
#print(sorted(demandas_productos))

while iteracion <= 10:
    zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda)
    #print(zonas_ordenadas[254].productos)
    #print(zonas_ordenadas[0].productos)
    demandas = [x.demanda for x in zonas_ordenadas]
    std_dev = int(stat.stdev(demandas))

    largo_it = len(str(iteracion))
    text_2 = ((3-largo_it)*" ") + str(iteracion) + ": " + str(std_dev)
    print(text_1 + text_2)

    #Comienza Algoritmo de swap Fase 1
    #print([x.demanda for x in ordenadas])
    for i in range(127):
        emparejar_zonas(zonas_ordenadas[i], zonas_ordenadas[254-i])
    #Termina Algoritmo de swap Fase 1

    iteracion += 1


distribucion_demandas = super.generar_heatmap()
min_5, max_5 = top_5(distribucion_demandas)
guardar_distribucion(super, min_5, max_5, "fase_1.txt")
index_list = max_5 + [0,0,0,0,0] + min_5
df = pd.DataFrame(np.array(distribucion_demandas), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=[str(x) for x in range(1,18)])

labels = df.applymap(lambda v: str(5 - (index_list.index(v)%10)) if v in index_list else '')

heat_map_2 = sns.heatmap(df, robust=True, linewidths=0.05, annot=labels, annot_kws={'fontsize':12}, fmt='', cmap="rocket_r", ax=ax2)

#plt.show()
