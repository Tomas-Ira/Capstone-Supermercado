from data_work import ordenados
from model import *
from heatmap import heatmap_de_super, heatmap_de_super_pasillos, generar_figura_completa

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

def asignar_zona_uniforme(pasillos, zona):
    #Primero busco a que pasillo agregar la zona -> el con menor demanda
    posicion = -1
    min = 1000000
    for i in range(len(pasillos)):
        pasillo = pasillos[i]
        if i < 15:
            if len(pasillo.zonas) < 8:
                if pasillo.demanda < min:
                    min = pasillo.demanda
                    posicion = i
        else:
            if len(pasillo.zonas) < 9:
                if pasillo.demanda < min:
                    min = pasillo.demanda
                    posicion = i

    #Agrego la zona
    if posicion >= 0:
        pasillo = pasillos[posicion]
        pasillo.zonas.append(zona)
        pasillo.calcular_demanda()

super = Supermercado()
super.poblar_fase_0(ordenados)

#Generamos heatmaps
fig = generar_figura_completa(super, 'Problema Supermercado - Fase 0')
show_all = input("Desea generar todos los heatmaps?\nYes --> 1\nNo ---> Cualquier tecla\nInput: ")
if show_all == "1":
    show_all = True
#Heatmaps listos

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

zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda)
#print(zonas_ordenadas[254].productos)
#print(zonas_ordenadas[0].productos)
demandas = [x.demanda for x in zonas_ordenadas]
std_dev = int(stat.stdev(demandas))

largo_it = len(str(iteracion))
text_2 = ((3-largo_it)*" ") + str(iteracion) + ": " + str(std_dev)
print(text_1 + text_2)

while iteracion < 5:
    iteracion += 1

    #Comienza Algoritmo de swap Fase 1
    #print([x.demanda for x in ordenadas])
    zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda)
    for i in range(127):
        emparejar_zonas(zonas_ordenadas[i], zonas_ordenadas[254-i])
    #Termina Algoritmo de swap Fase 1

    if show_all:
        fig = generar_figura_completa(super, 'Problema Supermercado - Iteracion ' + str(iteracion))

    #print(zonas_ordenadas[254].productos)
    #print(zonas_ordenadas[0].productos)
    demandas = [x.demanda for x in zonas_ordenadas]
    std_dev = int(stat.stdev(demandas))

    largo_it = len(str(iteracion))
    text_2 = ((3-largo_it)*" ") + str(iteracion) + ": " + str(std_dev)
    print(text_1 + text_2)



#Asignacion uniforme a pasillos
zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda, reverse=True)

pasillos = [Pasillo(x+1) for x in range(30)]

for i in range(30):
    pasillos[i].zonas.append(zonas_ordenadas[i])
    pasillos[i].calcular_demanda()

for i in range(30, 255):
    asignar_zona_uniforme(pasillos, zonas_ordenadas[i])

for i in range(15):
    pasillo_original = pasillos[i]
    pasillo_desechable = pasillos[i+15]
    for z in pasillo_desechable.zonas:
        pasillo_original.zonas.append(z)

super.pasillos = pasillos[:15]
#Finaliza asignacion a pasillos

fig = generar_figura_completa(super, 'Problema Supermercado - Fase 1')
plt.show()
