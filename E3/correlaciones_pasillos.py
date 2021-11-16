import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
from Reader import *
from model import *
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from random import sample, seed

def generar_muestra(numero):
    datos_todos = leer_datos()
    seed()
    return sample(datos_todos, numero)

supermercado = fase_0()
supermercado = fase_1(supermercado)
supermercado = fase_2(supermercado)


correlaciones = []
for i in range(27):
    correlaciones.append([])
for i in range(27):
    for j in range(27):
        correlaciones[i].append(0)

boletas = leer_datos()
print('Numero de boletas:', len(boletas))
primero = True
contador = 0
for boleta in boletas:
    visitas = contador_visitas_por_pasillo(supermercado, [boleta])
    visitas = visitas[0] + visitas[1]
    for i in range(27):
        pasillo_1 = visitas[i]
        if pasillo_1 == 1:
            for j in range(27):
                pasillo_2 = visitas[j]
                if pasillo_1 == 1 and pasillo_2 == 1:
                    correlaciones[i][j] += 1
    contador += 1
    if contador in [44081, 22041]:
        print('Llevamos:', contador)
    

indices = []
for i in range(1,16):
    indices.append('P' + str(i) + 'A')
for i in range(1,13):
    indices.append('P' + str(i) + 'B')

df = pd.DataFrame(np.array(correlaciones), 
                columns = indices,
                index=indices)

color = sns.color_palette("rocket_r", as_cmap=True)
heat_map = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap=color)
plt.show()

