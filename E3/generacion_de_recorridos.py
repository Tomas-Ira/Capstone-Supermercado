from fx_swap_pasillos import *

def gen_super_disperso(supermercado):
    '''
    Recibe un supermercado original post-fase 2 y lo reordena tal que quede disperso.
    '''
    swap_pasillos(supermercado, "A1", "A15")
    swap_pasillos(supermercado, "A2", "B12")
    return

def todas_combinaciones(supermercado, n=10):
    '''
    Define tres grupos, grupo grande 1, grupo grande 2 y trio de grupos morados. Los cambia en todas sus iteraciones posibles,
    '''
    lista_distancias = []
    posA1 = "A1"
    posA2 = "A2"
    pos1 = "A3"
    pos2 = "A4"
    pos3 = "A5"
    boletas = generar_muestra(n)
    # Primer grupo.
    for i in range(0, 24):
        if i < 12:
            if i == 0 or i == 1:
                posA1 = f"A{i+2}"
                swap_pasillos(supermercado, "A1", posA1)

                nom = f"A1-{posA1}"
                calcular_distancia(supermercado, nom, boletas)
                pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                lista_distancias.append(pack_distancia)

                swap_pasillos(supermercado, posA1, "A1")
                #print("i: ", posA1)
            else:
                pos = f"A{i+4}"
                swap_pasillos(supermercado, "A1", posA1)

                nom = f"A1-{posA1}"
                calcular_distancia(supermercado, nom, boletas)
                pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                lista_distancias.append(pack_distancia)

                swap_pasillos(supermercado, posA1, "A1")
                #print("i: ", posA1)
        else:
            pos = f"B{i-11}"
            swap_pasillos(supermercado, "A1", posA1)

            nom = f"A1-{posA1}"
            calcular_distancia(supermercado, nom, boletas)
            pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
            lista_distancias.append(pack_distancia)

            swap_pasillos(supermercado, posA1, "A1")
            #print("i: ", posA1)
        # Segundo grupo.
        for j in range(0, 24):
            if j < 12:
                if j == 0:
                    posA2 = f"A{j+1}"
                    swap_pasillos(supermercado, "A2", posA2)

                    nom = f"A2-{posA2}"
                    calcular_distancia(supermercado, nom, boletas)
                    pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                    lista_distancias.append(pack_distancia)

                    swap_pasillos(supermercado, posA2, "A2")
                    #print("  j: ", posA2)
                elif j == 1:
                    posA2 = f"A{j+2}"
                    swap_pasillos(supermercado, "A2", posA2)

                    nom = f"A2-{posA2}"
                    calcular_distancia(supermercado, nom, boletas)
                    pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                    lista_distancias.append(pack_distancia)

                    swap_pasillos(supermercado, posA2, "A2")
                    #print("  j: ", posA2)
                else:
                    pos = f"A{j+4}"
                    swap_pasillos(supermercado, "A2", posA2)

                    nom = f"A2-{posA2}"
                    calcular_distancia(supermercado, nom, boletas)
                    pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                    lista_distancias.append(pack_distancia)

                    swap_pasillos(supermercado, posA2, "A2")
                    #print("  j: ", posA2)
            else:
                posA2 = f"B{j-11}"
                swap_pasillos(supermercado, "A2", posA2)

                nom = f"A2-{posA2}"
                calcular_distancia(supermercado, nom, boletas)
                pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                lista_distancias.append(pack_distancia)

                swap_pasillos(supermercado, posA2, "A2")
                #print("  j: ", posA2)
            # Tercer grupo.
            for k in range(0, 22):
                if k < 12:
                    if k == 0 or k == 1:
                        pos1 = f"A{k+1}"
                        pos2 = f"A{k+2}"
                        pos3 = f"A{k+3}"
                        swap_pasillos(supermercado, "A3", pos1)
                        swap_pasillos(supermercado, "A4", pos2)
                        swap_pasillos(supermercado, "A5", pos3)

                        nom = f"A3-{pos1}"
                        calcular_distancia(supermercado, nom, boletas)
                        pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                        lista_distancias.append(pack_distancia)

                        swap_pasillos(supermercado, pos1, "A3")
                        swap_pasillos(supermercado, pos2, "A4")
                        swap_pasillos(supermercado, pos3, "A5")
                        #print("    k: ", pos1, pos2, pos3)
                    else:
                        pos1 = f"A{k+2}"
                        pos2 = f"A{k+3}"
                        pos3 = f"A{k+4}"
                        swap_pasillos(supermercado, "A3", pos1)
                        swap_pasillos(supermercado, "A4", pos2)
                        swap_pasillos(supermercado, "A5", pos3)

                        nom = f"A3-{pos1}"
                        calcular_distancia(supermercado, nom, boletas)
                        pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                        lista_distancias.append(pack_distancia)

                        swap_pasillos(supermercado, pos1, "A3")
                        swap_pasillos(supermercado, pos2, "A4")
                        swap_pasillos(supermercado, pos3, "A5")
                        #print("    k: ", pos1, pos2, pos3)
                else:
                    pos1 = f"B{k-11}"
                    pos2 = f"B{k-10}"
                    pos3 = f"B{k-9}"
                    swap_pasillos(supermercado, "A3", pos1)
                    swap_pasillos(supermercado, "A4", pos2)
                    swap_pasillos(supermercado, "A5", pos3)

                    nom = f"A3-{pos1}"
                    calcular_distancia(supermercado, nom, boletas)
                    pack_distancia = [posA1, posA2, pos1, supermercado.prom_distancia]
                    lista_distancias.append(pack_distancia)

                    swap_pasillos(supermercado, pos1, "A3")
                    swap_pasillos(supermercado, pos2, "A4")
                    swap_pasillos(supermercado, pos3, "A5")
                    #print("    k: ", pos1, pos2, pos3)
    return lista_distancias
    
def print_lista_todas_combinaciones(list_distancias):
    '''
    Imprime la lista de distancias ORDENADA generada en la función todas combinaciones en un archivo llamado 
    "Archivos Distancias/todas_combinaciones.txt".
    '''

    with open("Archivos Distancias/todas_combinaciones.txt", "w") as f:
        for linea in list_distancias:
            f.write("PosA1: " + linea[0] + " PosA2: " + linea[1] + " PosA3: " + linea[2] 
            + " ---> Distancia Promedio: " + str(linea[3]) + "\n")

def generador_de_supermercados(supermercado, posA1, posA2, posA3_1, posA3_2, posA3_3):
    # PosA1
    swap_pasillos(supermercado, "A1", posA1)
    # PosA2
    swap_pasillos(supermercado, "A2", posA2)
    # PosA3
    swap_pasillos(supermercado, "A3", posA3_1)
    swap_pasillos(supermercado, "A4", posA3_2)
    swap_pasillos(supermercado, "A5", posA3_3)