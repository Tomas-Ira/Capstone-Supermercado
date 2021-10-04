from data_work import rows
from model import *
from Reader import *

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))
fig.suptitle('Problema Supermercado - Distribución caso base', fontsize=18)
ax1.set_title("Heatmap por zonas")
ax2.set_title("Heatmap por pasillos")

super = Supermercado()
super.poblar(rows)
distribucion_demandas = super.generar_heatmap()
min_5, max_5 = top_5(distribucion_demandas)
guardar_distribucion(super, min_5, max_5, "distribucion.txt")
#print(super.match_pasillos([48, 65, 865, 413]))
#print(contador_visitas_por_pasillo(super, [[48, 65, 865, 413]]))
#print(distancia_recorrida(super, [48, 65, 865, 413]))
index_list = max_5 + [0,0,0,0,0] + min_5
df = pd.DataFrame(np.array(distribucion_demandas), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=[str(x) for x in range(1,18)])

labels = df.applymap(lambda v: str(5 - (index_list.index(v)%10)) if v in index_list else '')

heat_map_1 = sns.heatmap(df, robust=True, linewidths=0.05, annot=labels, annot_kws={'fontsize':12}, fmt='', cmap="rocket_r", ax=ax1)

distribucion_demandas_por_pasillo = super.heatmap_pasillos()
df_pasillos = pd.DataFrame(np.array(distribucion_demandas_por_pasillo), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=['A', 'B'])

heat_map_2 = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r", ax=ax2)

# Calcular distancia
boletas = generar_muestra(1000)
visitas_por_pasillo = contador_visitas_por_pasillo(super, boletas)
distancias = [distancia_recorrida(super, x) for x in boletas]
distancias_clean = [i for i in distancias if i!= 0]
promedio = str(int(stat.mean(distancias_clean)))
print("Distancia promedio: " + promedio)
print("Distancia max: " + str(max(distancias_clean)))
print("Distancia min: " + str(min(distancias_clean)))
#

df_pasillos_muestra = pd.DataFrame(np.array(visitas_por_pasillo), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=['A', 'B'])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))
fig.suptitle('Problema Supermercado - Comparación muestral vs teórica', fontsize=18)
ax1.set_title("Heatmap teórico")
ax2.set_title("Heatmap muestral")

heat_map_2 = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r", ax=ax1)
heat_map_3 = sns.heatmap(df_pasillos_muestra, robust=True, linewidths=0.05, cmap="rocket_r", ax=ax2)

#plt.show()