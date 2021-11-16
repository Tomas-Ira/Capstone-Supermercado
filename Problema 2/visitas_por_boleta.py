from data_work import ordenados
from model import *
from heatmap import heatmap_de_super_pasillos_estacional
from Reader import *

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

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

iteracion = 0

zonas = []
for pasillo in super.pasillos:
    for zona in pasillo.zonas:
        zonas.append(zona)

demandas_productos = []
for z in zonas:
    for p in z.productos:
        demandas_productos.append(int(p[1]))

while iteracion < 5:
    iteracion += 1

    #Comienza Algoritmo de swap Fase 1
    #print([x.demanda for x in ordenadas])
    zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda)
    for i in range(114):
        emparejar_zonas(zonas_ordenadas[i], zonas_ordenadas[227-i])
    #Termina Algoritmo de swap Fase 1
    
zonas_ordenadas = sorted(zonas, key=lambda x: x.demanda, reverse=True)

pasillos = [Pasillo(x+1) for x in range(27)]

for i in range(27):
    pasillos[i].zonas.append(zonas_ordenadas[i])
    pasillos[i].calcular_demanda()

for i in range(27, 228):
    asignar_zona_uniforme(pasillos, zonas_ordenadas[i])

for i in range(12):
    pasillo_original = pasillos[i]
    pasillo_desechable = pasillos[i+15]
    for z in pasillo_desechable.zonas:
        pasillo_original.zonas.append(z)
        
super.pasillos = pasillos[:15]
super_fase1 = super

htmap = heatmap_de_super_pasillos_estacional(super)
#heat_map = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r")
plt.show()
