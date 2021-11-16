from data_work import ordenados
from model import *

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import csv

def swap_pasillos(super, p1, p2):
    '''
    Esta función se encarga de cambiar las posiciones de dos pasillos.
    IMPORTANTE: el formato de cada pasillo se recibe como string como los siguientes ejemplos:
    'A3', 'B1', 'A12' ...
    
    INPUT:
    * super -> class Supermercado()
    * p1 -> string
    * p2 -> string
    
    OUTPUT:
    * None
    
    Nota: Si se cambia un pasillo superior con uno inferior, solo se cambian las primeras 8 secciones
    '''
    
    #En primer lugar determinamos si cada pasillo corresponde a uno superior o inferior
    p1_superior = False
    if 'A' in p1:
        p1_superior = True
    
    p2_superior = False
    if 'A' in p2:
        p2_superior = True
        
    #Obtenemos el número de cada pasillo
    p1_number = int(p1.strip('AB')) - 1
    p2_number = int(p2.strip('AB')) - 1
    
    #Obtenemos cada pasillo
    p1 = super.pasillos[p1_number]
    p2 = super.pasillos[p2_number]
    
    #Creamos un respaldo con las zonas de p1 que cambiaremos
    #Si p1 es superior cambias las primeras 8
    respaldo_p1 = []
    for i in range(len(p1.zonas)):
        if p1_superior:
            if i < 8:
                respaldo_p1.append(p1.zonas[i])
        else:
            if i > 7 and i < 16:
                respaldo_p1.append(p1.zonas[i])
                
    #Repetimos con p2
    respaldo_p2 = []
    for i in range(len(p2.zonas)):
        if p2_superior:
            if i < 8:
                respaldo_p2.append(p2.zonas[i])
        else:
            if i > 7 and i < 16:
                respaldo_p2.append(p2.zonas[i])
                
    #Hacemos los swaps para p1
    for i in range(len(p1.zonas)):
        if p1_superior:
            if i < 8:
                p1.zonas[i] = respaldo_p2[i]
        else:
            if i > 7 and i < 16:
                p1.zonas[i] = respaldo_p2[i-8]
                
    #Hacemos los swaps para p2
    for i in range(len(p2.zonas)):
        if p2_superior:
            if i < 8:
                p2.zonas[i] = respaldo_p1[i]
        else:
            if i > 7 and i < 16:
                p2.zonas[i] = respaldo_p1[i-8]
            
    
    