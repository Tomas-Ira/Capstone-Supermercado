import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
from Reader import generar_muestra
from model import *
from fx_fase0 import *
from fx_fase1 import *
from fx_fase2 import *
from random import sample, seed
import csv
from correlaciones_secciones import *

def generar_swaps_secciones(n, supermercado, correlaciones, n_boletas, simulada, path_boletas_simuladas):
    '''
    Esta funcion genera n swaps de secciones en base a los valores de correlaciones entre estas
    
    INPUT:
    * n -> int con el largo de la lista que se quiere retornar
    * supermercado -> Supermercado() despues de fase 2
    * correlaciones -> matriz de 228 x 228 con correlaciones de secciones
    '''
    boletas = generar_muestra(n_boletas, simulada, False, path_boletas_simuladas)

    with open('Archivos Correlaciones/correlaciones_secciones.csv', 'r') as file:
        csvreader = csv.reader(file)
        swaps = 0
        set_inamovibles = set()
        nuevos_codigos = {}
        cont = 0
        while swaps < n:
            cont += 1
            #print(nuevos_codigos, '\n')
            info = next(csvreader)
            print(f'{cont}. Intento de hacer el swap ' + str(swaps + 1) + 'º\n')
            #print(info, '\n')
            '''Determinamos que zonas requieren swap'''
            cod1 = info[0]
            cod2 = info[1]
            if cod1 in nuevos_codigos.keys():
                cod1 = nuevos_codigos[cod1]
            if cod2 in nuevos_codigos.keys():
                cod2 = nuevos_codigos[cod2]
            estatico = zona_estatica(supermercado, cod1, cod2)
            if estatico == cod1:
                zona_de_swap_1 = cod2
            else:
                zona_de_swap_1 = cod1
            zona_de_swap_2 = seccion_menor_correlacion(estatico, correlaciones=correlaciones)
            if not(zona_de_swap_1 in set_inamovibles or zona_de_swap_2 in set_inamovibles):
                #print("Hacemos el swap", zona_de_swap_1, zona_de_swap_2,'\n')
                '''Hacemos el swap entre ambas secciones'''
                swap_secciones(supermercado, zona_de_swap_1, zona_de_swap_2)
                swaps += 1
                '''Recalculamos correlaciones entre secciones'''
                correlaciones = create_correlaciones_matrix()
                correlaciones = load_correlaciones_sec(supermercado, correlaciones, boletas)
                '''Agregamos estatico y zonas de swap al set de inamovibles'''
                set_inamovibles.add(estatico)
                set_inamovibles.add(zona_de_swap_2)
                nuevos_codigos[zona_de_swap_1] = zona_de_swap_2
                nuevos_codigos[zona_de_swap_2] = zona_de_swap_1
            else:
                #print('***** SWAP FALLIDO *****')
                #print('No se hace el swap', estatico, zona_de_swap_1, zona_de_swap_2)
                #print(set_inamovibles, '\n')
                pass
        
#obtener_listado_de_swaps(1)

def seccion_menor_correlacion(codigo, correlaciones):
    '''
    Esta funcion recibe un codigo de una seccion y retorna el codigo de
    la seccion que tiene menor correlacion con esta y se encuentra en el mismo pasillo.
    
    INPUT:
    * codigo -> string de formato 'P1A-1'
    
    OUTPUT:
    * string de formato 'P1A-1'
    '''
    seccion = int(codigo.split('-')[1])
    pasillo = int(codigo.split('-')[0].strip('PAB'))
    posicion = codigo_a_numero(codigo)
    fila = correlaciones[posicion]
    #print(fila, '\n')
    inicio_pasillo = 0
    fin_pasillo = 0
    if pasillo <= 12 :
        inicio_pasillo += (pasillo - 1) * 17
    else:
        inicio_pasillo += 12 * 17
        inicio_pasillo += (pasillo - 13) * 8
    if seccion <= 8:
        fin_pasillo = inicio_pasillo + 8
    else:
        fin_pasillo = inicio_pasillo + 17
        inicio_pasillo += 8
    lista_pasillo = fila[inicio_pasillo:fin_pasillo]
    #print(lista_pasillo, '\n')
    contador = 0
    minimo = 100000
    posicion_minimo = -1
    seccion_local = seccion
    if seccion >= 8:
        seccion_local -= 8
    for i in range(len(lista_pasillo)):
        contador += 1
        if contador != seccion_local:
            if lista_pasillo[i] < minimo:
                minimo = lista_pasillo[i]
                posicion_minimo = i
    #print(posicion_minimo, '\n')
    codigo_final = codigo.split('-')[0] + '-' + str(posicion_minimo + 1)
    if seccion <= 8:
        codigo_final = codigo.split('-')[0] + '-' + str(posicion_minimo + 1)
    else:
        codigo_final = codigo.split('-')[0] + '-' + str(posicion_minimo + 1 + 8)
    #print(codigo_final, '\n')
    return codigo_final

def codigo_a_numero(codigo):
    '''
    Esta funcion recibe el codigo de un pasillo y retorna el numero al que este corresponde
    en la matriz de correlaciones. Hay 228 secciones, pero se retorna la posicion, es decir el
    numero -1. Ej: la ultima seccion 228, se retornaria 227.
    
    INPUT:
    * codigo -> string de formato 'P1A-1'
    
    OUTPUT:
    * int
    '''
    codigo = codigo.strip('P')
    valores = codigo.split('-')
    valores[0] = int(valores[0].strip('AB'))
    valores[1] = int(valores[1])
    posicion = 0
    if valores[0] <= 12 :
        posicion += (valores[0] - 1) * 17
    else:
        posicion += 12 * 17
        posicion += (valores[0] - 13) * 8
    posicion += valores[1] - 1
    return posicion

def zona_estatica(supermercado, cod1, cod2):
    '''
    Recibe dos códigos de zonas y retorna el código que queda estático.

    OUTPUT:
    cod1 o cod2, dependiendo de qué zona posee más demanda.
    '''
    # Primero buscamos el código de pasillo de cada código:
    cod_pas1 = int(cod1[1])
    cod_pas2 = int(cod2[1])

    # Ahora buscamos el pasillo correspondiente en la lista de pasillos del supermercado.
    pas1 = supermercado.pasillos[cod_pas1 - 1]
    pas2 = supermercado.pasillos[cod_pas2 - 1]

    # Teniendo el pasillo, buscamos la zona.

    # Para eso, primero separamos el string según su '-'
    _, cod_zona1 = cod1.split("-")
    _, cod_zona2 = cod2.split("-")
    
    # Finalmente obtenemos las zonas
    zona1 = pas1.zonas[int(cod_zona1) - 1]
    zona2 = pas2.zonas[int(cod_zona2) - 1]

    # Por último, retornamos la que tenga MÁS demanda de las 2:
    if zona1.demanda > zona2.demanda:
        return cod1
    else:
        return cod2
    
def swap_secciones(supermercado, cod1, cod2):
    '''
    Recibe dos códigos de secciones de un supermercado, y los cambia entre sí.
    Recalcula demanda de pasillos en cuestión y distancia de supermercado.

    OUTPUT
    None
    '''
    # Primero buscamos el código de pasillo de cada código:
    cod_pas1 = int(cod1[1])
    cod_pas2 = int(cod2[1])

    # Ahora buscamos el pasillo correspondiente en la lista de pasillos del supermercado.
    pas1 = supermercado.pasillos[cod_pas1 - 1]
    pas2 = supermercado.pasillos[cod_pas2 - 1]

    # Teniendo el pasillo, buscamos la zona.
    # Para eso, primero separamos el string según su '-'
    _, cod_zona1 = cod1.split("-")
    _, cod_zona2 = cod2.split("-")
    
    # Finalmente we retrieve las zonas
    zona1 = pas1.zonas[int(cod_zona1) - 1]
    zona2 = pas2.zonas[int(cod_zona2) - 1]

    # Antes de cambiar, preparamos el swap cambiando el id de las zonas:
    id_zona1 = zona1.id
    zona1.id = zona2.id
    zona2.id = id_zona1

    # Luego, hacemos el swap entre listas
    list_swapper(pas1.zonas, int(cod_zona1) - 1, pas2.zonas, int(cod_zona2) - 1)

    # También recalculamos la demanda de los pasillos en cuestión.
    pas1.calcular_demanda()
    pas2.calcular_demanda()

    return

def list_swapper(list1, indice1, list2, indice2):
    '''
    Recibe dos índices y de dos listas (respectivamente, o sea, indice1 -> list1 y viceversa).
    Retorna ambas listas con los ítems de cada indice swapeados.

    EJEMPLO:
    list1: [1, 2, 3]        
    indice1: 2              list1: [1, 2, a]
                        -->  
    list2: [a, b, c]        list2: [3, b, c]
    indice2: 0              

    OUTPUT:
    list1, list2
    '''
    list1[indice1], list2[indice2] = list2[indice2], list1[indice1]
    return list1, list2
