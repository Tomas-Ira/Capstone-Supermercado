from os import replace
from model import *

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

def creador_de_matriz(supermercado):
    return

def algoritmo_correlaciones_2(path):
    '''
    INPUT: la lista puede ser de pasillo o de zonas.
    '''
    posiciones_superiores = []
    posiciones_inferiores = []
    correlaciones = []
    with open(path, "r") as file:
        for linea in file:
            linea_list = linea.strip().split(",")
            correlaciones.append(linea_list)
    



    return 
