from os import replace
from model import *
import os

def zonas_pasillo_dividido(supermercado, pasillo_code):
    '''
    Función que recibe un 'pasillo_code' (ej. 'P1A') y un supermercado, y retorna la lista de zonas que corresponden a ese pasillo.
    '''
    id = pasillo_code.replace("P", "")
    id = int(id[:-1])
    
    if pasillo_code[-1] == 'A':
        return supermercado.pasillos[id-1].zonas[:8] #primeras 8 zonas
    else:
        return supermercado.pasillos[id-1].zonas[8:] #últimas 9 zonas

def algoritmo_correlaciones(supermercado):

    # Creamos un dos listas, una para pasillo superiores y otra para inferiores
    pasillos_superiores = [Pasillo(x+1) for x in range(15)]
    pasillos_inferiores = [Pasillo(x+1) for x in range(15, 30)]

    # Ponemos los pasillos estacionales por defecto en las últimas posiciones de los pasillos inferiores.
    pasillos_inferiores[12].zonas = zonas_pasillo_dividido(supermercado, "P13B")
    pasillos_inferiores[13].zonas = zonas_pasillo_dividido(supermercado, "P14B")
    pasillos_inferiores[14].zonas = zonas_pasillo_dividido(supermercado, "P15B") # Recordar que los índices parten desde 0.

    pasillos_ya_cargados = set() # set que guarda CÓDIGOS (ej. 'P1A') de pasillos ya cargados
    puesto_sup = 0
    puesto_inf = 0
    # Cargamos los pasillos
    path = "Archivos Correlaciones/correlaciones_pasillos.csv"
    with open(path, "r") as file:
        for linea in file:
            # Limpiamos la línea y la guardamos en variables
            cod1, cod2, corr = linea.strip().split(',')
            # Si ya se llenó todo el pasillo, paramos
            if len(pasillos_ya_cargados) == 27:
                break
            # Para el segundo código (es segundo y dps primero, el orden importa)
            if cod2 not in pasillos_ya_cargados:
                zonas = zonas_pasillo_dividido(supermercado, cod2)
                if cod2[-1] == "A": # se pone arriba
                    if puesto_sup < 15:
                        pasillos_superiores[puesto_sup].zonas = zonas
                        pasillos_inferiores[puesto_sup].calcular_demanda()
                        puesto_sup += 1
                        pasillos_ya_cargados.add(cod2)
                else: # se pone abajo
                    if puesto_inf < 12:
                        pasillos_inferiores[puesto_inf].zonas = zonas
                        pasillos_inferiores[puesto_inf].calcular_demanda()
                        puesto_inf += 1
                        pasillos_ya_cargados.add(cod2)

            # Para el primer código, que puede ser E
            if cod1 == "E":
                pass
            else:
                if cod1 not in pasillos_ya_cargados:
                    zonas = zonas_pasillo_dividido(supermercado, cod1)
                    if cod1[-1] == "A": # se pone arriba
                        if puesto_sup < 15:
                            pasillos_superiores[puesto_sup].zonas = zonas
                            pasillos_inferiores[puesto_sup].calcular_demanda()
                            puesto_sup += 1
                            pasillos_ya_cargados.add(cod1)
                    else: # se pone abajo
                        if puesto_inf < 12:
                            pasillos_inferiores[puesto_inf].zonas = zonas
                            pasillos_inferiores[puesto_inf].calcular_demanda()
                            puesto_inf += 1
                            pasillos_ya_cargados.add(cod1)

    #Agregamos zonas de pasillos inferiores a pasillos superiores (por consistencia con el modelo Supermercado)
    for i in range(15):
        pasillo_sup = pasillos_superiores[i]
        pasillo_inf = pasillos_inferiores[i]
        for z in pasillo_inf.zonas:
            pasillo_sup.zonas.append(z)

    supermercado.pasillos = pasillos_superiores[:15]

    return supermercado

def indice_mas_cercano(posiciones, esta_indice):
    top = esta_indice
    bot = esta_indice
    if posiciones[esta_indice] == -1:
        return esta_indice
    while top < len(posiciones) and bot >= 0:
        if top == len(posiciones) - 1 and bot == 0:
            return "pendiente"
        elif top == len(posiciones) - 1 and bot != 0:
            return len(posiciones)
        elif top != len(posiciones) - 1 and bot == 0:
            return 0
        elif posiciones[top + 1] == -1 and posiciones[bot - 1] == -1:
            return "pendiente"
        elif posiciones[top + 1] == -1 and posiciones[bot - 1] != -1:
            return top + 1
        elif posiciones[top + 1] != -1 and posiciones[bot - 1] == -1:
            return bot - 1
        top += 1
        bot -= 1

#def loader_correlaciones(path="./E3/Archivos Correlaciones/correlaciones_pasillos.csv"):
def loader_correlaciones(path="Archivos Correlaciones/correlaciones_pasillos.csv"):
    '''
    Lee el archivo de correlaciones y lo carga en una lista.
    '''
    correlaciones = []
    with open(path, "r") as file:
        for linea in file:
            linea_list = linea.strip().split(",")
            correlaciones.append(linea_list)
    return correlaciones


def insertar(posiciones, cercano, falta, otras_posiciones):
    if cercano < len(posiciones):
        if posiciones[cercano] == -1:
            posiciones[cercano] = falta
            return posiciones, otras_posiciones

    posiciones.insert(cercano, falta)

    if cercano == 0:
        otras_posiciones.insert(cercano,-1)

    return posiciones, otras_posiciones
    

def algoritmo_correlaciones(path="Archivos Correlaciones/correlaciones_pasillos.csv"):

    # Primero cargamos los datos del archivo de correlaciones
    correlaciones = loader_correlaciones()

    posiciones_sup = []
    posiciones_inf = []
    ya_ingresados = set()

    pas1 = correlaciones[0][0]
    pas2 = correlaciones[0][1]
    posiciones_sup.append(pas1)
    posiciones_sup.append(pas2)
    posiciones_inf.append(-1)
    posiciones_inf.append(-1)
    ya_ingresados.add(pas1)
    ya_ingresados.add(pas2)
    correlaciones.pop(0)

    i = 0
    while len(ya_ingresados) < 27:
        cod1, cod2, cantidad = correlaciones[i]

        #print("PASILLO SUPERIOR:", posiciones_sup)
        #print("PASILLO INFERIOR:", posiciones_inf)
        #print("CÓDIGOS: ", cod1 , cod2, cantidad)
        #print("-"*45)
        #print("")

        if cod1 in ya_ingresados and cod2 in ya_ingresados: 
            i += 1
            continue

        if cod1 not in ya_ingresados and cod2 not in ya_ingresados:
            i += 1
            continue

        elif cod1 in ya_ingresados:
            esta = cod1
            falta = cod2

        elif cod2 in ya_ingresados:
            esta = cod2
            falta = cod1
        
        completo_sup = len(posiciones_sup) == 15
        completo_inf = len(posiciones_inf) == 12
        
        if falta[-1] == "B":
            if esta[-1] == "B":
                indice = posiciones_inf.index(esta)
            if esta[-1] == "A":
                indice = posiciones_sup.index(esta)

            cercano = indice_mas_cercano(posiciones_inf, indice)

            if completo_inf or completo_sup:
                while cercano == 0:
                    indice += 2
                    cercano = indice_mas_cercano(posiciones_inf, indice)
                     # Podria Fallar

                if completo_inf:
                    while cercano == len(posiciones_inf):
                        indice -= 1
                        cercano = indice_mas_cercano(posiciones_inf, indice)

            if cercano == "pendiente":
                if i == 1:
                    cercano = indice_mas_cercano(posiciones_inf, indice-1)
                else:
                    i += 1
                    continue
            
            posiciones_inf, posiciones_sup = insertar(posiciones_inf, cercano, falta, posiciones_sup)
            ya_ingresados.add(falta)
            correlaciones.pop(i)
            i = 0
        
        if falta[-1] == "A":
            if esta[-1] == "B":
                indice = posiciones_inf.index(esta)
            if esta[-1] == "A":
                indice = posiciones_sup.index(esta)
            
            cercano = indice_mas_cercano(posiciones_sup, indice)

            if completo_inf or completo_sup:
                while cercano == 0:
                    indice += 1
                    cercano = indice_mas_cercano(posiciones_sup, indice)
                    # Podria Fallar

                if completo_sup:
                    while cercano == len(posiciones_sup):
                        indice -= 1
                        cercano = indice_mas_cercano(posiciones_sup, indice)

            if cercano == "pendiente":
                if i == 1:
                    cercano = indice_mas_cercano(posiciones_sup, indice-1)
                else:
                    i += 1
                    continue

            posiciones_sup, posiciones_inf = insertar(posiciones_sup, cercano, falta, posiciones_inf)
            ya_ingresados.add(falta)
            correlaciones.pop(i)
            i = 0

    posiciones_inf.append('P13B')
    posiciones_inf.append('P14B')
    posiciones_inf.append('P15B')
    
    return posiciones_sup, posiciones_inf

def pasillo_positioner(supermercado, posiciones_inf, posiciones_sup):
    '''
    INPUTS
     * supermercado
     * posiciones_inf: lista con códigos de pasillos inferiores.
     * posiciones_sup: lista con códigos de pasillos superiores.

     Mueve los pasillos de 'supermercado' inicial, según las asignaciones de pasillos de las listas.
    '''
    # Creamos un dos listas, una para pasillo superiores y otra para inferiores
    pasillos_superiores = [Pasillo(x+1) for x in range(15)]
    pasillos_inferiores = [Pasillo(x+1) for x in range(15, 30)]

    # Posiciones inferiores
    for i in range(0, 15):
        pasillos_inferiores[i].zonas = zonas_pasillo_dividido(supermercado, posiciones_inf[i])
        pasillos_superiores[i].zonas = zonas_pasillo_dividido(supermercado, posiciones_sup[i])
    
    #Agregamos zonas de pasillos inferiores a pasillos superiores (por consistencia con el modelo Supermercado)
    for i in range(15):
        pasillo_sup = pasillos_superiores[i]
        pasillo_inf = pasillos_inferiores[i]
        for z in pasillo_inf.zonas:
            pasillo_sup.zonas.append(z)

    supermercado.pasillos = pasillos_superiores[:15]
    for p in supermercado.pasillos:
        p.calcular_demanda()

    return supermercado
