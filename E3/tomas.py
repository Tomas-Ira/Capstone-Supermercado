from collections import defaultdict
import csv
import random
import matplotlib.pyplot as plt
from scipy.stats import chisquare

ESPACIOS = 12750
CLUSTERS = 85
TEMPORADAS = 3

all_tickets = dict()
all_products = dict()


class Ticket:
    def __init__(self, id):
        self.id = id
        self.products = set()

    def add_product(self, product):
        self.products.add(product.id)
        product.add_ticket(self)


class Product:
    def __init__(self, id):
        self.id = id
        self.tickets = set()
        self.popularity = 0  # Muestra en cuantas boletas aparece un producto
        self.seasons = {i: False for i in range(TEMPORADAS)}
        self.estacional = False

    def add_ticket(self, ticket):
        self.tickets.add(ticket)
        self.popularity += 1

    @property
    def periodos_tot(self):
        contador = 0
        for i in self.seasons:
            if self.seasons[i]:
                contador += 1
        return contador


def leer_datos():
    ventas = 0
    DATA = [i.strip().split() for i in open("./Data/retail.dat").readlines()]
    for tic in range(len(DATA)):
        new_ticket = Ticket(tic)
        all_tickets[tic] = new_ticket
        for prod in DATA[tic]:
            ventas += 1
            if prod not in all_products:
                all_products[prod] = Product(prod)
            new_ticket.add_product(all_products[prod])
    return ventas


def aparece_x_temporadas():
    aparece_x_temporada = {i: [] for i in range(1, TEMPORADAS+1)}

    for pid in all_products:
        aparece_x_temporada[all_products[pid].periodos_tot].append(
            all_products[pid])

    return aparece_x_temporada


def fase_1():
    aparece_x_temporada = aparece_x_temporadas()
    posiciones = {i: [False]*TEMPORADAS for i in range(ESPACIOS)}
    contador = 0
    terminar = False
    usadas = 0

    for pos in range(ESPACIOS):
        for temp in range(TEMPORADAS):
            for prod in aparece_x_temporada[temp+1]:
                if encaja(posiciones[pos], prod) and not prod.estacional:
                    posiciones[pos] = agregar(posiciones[pos], prod)
                    prod.estacional = True
                    contador += 1
                    usadas += temp+1
                    break
            if len(all_products) - contador == ESPACIOS - pos:
                terminar = True
                break
        if terminar:
            break

    print("")
    print("DATOS----------")
    mostrar(aparece_x_temporada)
    print("Productos estacionales: ", contador)
    print("Posiciones estacionales: ", pos)
    # print("Ocupación promedio espacios estacionales: ", usadas/pos)

    print("Productos permanentes: ", len(all_products) - contador)
    print("Posiciones permanentes: ", ESPACIOS - pos)

    return posiciones


def mostrar(aparece_x_temporada):
    lista = {}
    for i in aparece_x_temporada:
        lista[i] = len(aparece_x_temporada[i])
    print(lista)


def encaja(pos, prod):
    for i in range(len(pos)):
        if pos[i]:
            if prod.seasons[i]:
                return False
    return True


def agregar(pos, prod):
    for i in prod.seasons:
        if prod.seasons[i]:
            pos[i] = prod.id
    return pos


def productos_permanentes():
    fase_1()
    permanenetes = []

    for pid in all_products:
        if not all_products[pid].estacional:
            permanenetes.append(pid)
    return permanenetes


# Imprimir análisis sobre productos y espacios temporales/permanentes
def analisis_datos():
    meses_vendidos = 0
    meses_perm = 0
    meses_temp = 0
    prod_temp = 0
    for pid in all_products:
        meses_vendidos += all_products[pid].periodos_tot
        if all_products[pid].estacional:
            prod_temp += 1
            meses_temp += all_products[pid].periodos_tot
        else:
            meses_perm += all_products[pid].periodos_tot

    print("Meses promedio que se vende 1 producto cualquiera: ",
          meses_vendidos/len(all_products))
    print("Meses promedio que se vende 1 producto escational: ", meses_temp/prod_temp)
    print("Meses promedio que se vende 1 producto permaente: ",
          meses_perm/(len(all_products) - prod_temp))


# Crear archivo con ids de productos permanentes
def escribir_uso_posiciones():
    permanentes = productos_permanentes()
    with open('Productos Permanentes.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        datos = ["ID"]
        writer.writerow(datos)
        for id in permanentes:
            datos = [id]
            writer.writerow(datos)


# Se llama en crear_boletas_n_prodcutos
def crear_distribucion_productos(tickets):
    productos = []
    for bid in tickets:
        for pid in tickets[bid].products:
            productos.append(pid)
    return productos


# Se llama en crear_n_boletas
def crear_boletas_n_productos(tickets, n):
    productos = crear_distribucion_productos(tickets)
    simulada = random.sample(productos, n)

    seen = set()
    for pid in simulada:
        if pid not in seen:
            seen.add(pid)
        else:
            new = random.sample(productos, 1)
            while new[0] in seen:
                new = random.sample(productos, 1)
            seen.add(new[0])
    return simulada


# Se llama en crear_n_boletas
def crear_largos(tickets):
    largos = []
    for bid in tickets:
        largos.append(len(tickets[bid].products))
    return largos


def crear_n_boletas(n, tickets):
    boletas_simuladas = dict()
    largos = crear_largos(tickets)

    for tic in range(n):
        cantidad = random.sample(largos, 1)
        boleta = crear_boletas_n_productos(tickets, cantidad[0])
        new_ticket = Ticket(tic)
        boletas_simuladas[tic] = new_ticket
        for prod in boleta:
            new_ticket.add_product(all_products[prod])

    return boletas_simuladas

def crear_distribucion(boletas):
    distribucion = {i: 0 for i in all_products}
    totales = 0
    for bid in boletas:
        for pid in boletas[bid].products:
            distribucion[pid] += 1
            totales += 1
    for prod in distribucion:
        distribucion[prod] = distribucion[prod]/totales

    return distribucion

def crear_listas(boletas):
    lista = []
    for bid in boletas:
        for pid in boletas[bid].products:
            lista.append(pid)
    return lista

def chi_cuadrado(boletas):
    dist_bol = crear_distribucion(boletas)
    dist_real = crear_distribucion(all_tickets)
    valor = 0
    for i in dist_real:
        valor += ((dist_real[i]-dist_bol[i])**2)/dist_real[i]

    return valor


def primeros_tickets(n):
    boletas = {}
    for i in range(n):
        boletas[i] = all_tickets[i]
    return boletas


def print_graph_simulado(n, tickets):
    boletas = crear_n_boletas(n, tickets)
    data = {str(i): 0 for i in range(len(all_products))}

    for bid in boletas:
        for pid in boletas[bid].products:
            data[pid] += 1
    names = list(data.keys())
    values = list(data.values())
    plt.bar(names, values)
    plt.show()


def print_graph_real():
    boletas = all_tickets
    valores = []
    for bid in boletas:
        for pid in boletas[bid].products:
            valores.append(pid)
    largo = len(set(valores))
    plt.hist(valores, largo)
    plt.show()


def indice_mas_cercano(posiciones, esta_indice):
    top = esta_indice
    bot = esta_indice
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


def algoritmo_correlaciones(correlaciones):
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
        cod1, cod2, _ = correlaciones[i]
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
        completo_inf = len(posiciones_sup) == 12
        
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

            if cercano == "pendiente":
                i += 1
                continue
                
            posiciones_inf.insert(cercano, falta)
            ya_ingresados.add(falta)
            correlaciones.pop(0)
            i = 0
            
            if cercano == 0:
                posiciones_sup.insert(cercano,-1)

            else:
                # Se agregó el producto al final o se remplazo por un -1
                continue
        
        if falta[-1] == "A":
            if esta[-1] == "B":
                indice = posiciones_inf.index(esta)
            if esta[-1] == "A":
                indice = posiciones_sup.index(esta)

            
            cercano = indice_mas_cercano(posiciones_sup, indice)

            if completo_inf or completo_sup:
                while cercano == 0:
                    indice += 2
                    cercano = indice_mas_cercano(posiciones_inf, indice)

            if cercano == "pendiente":
                i += 1
                continue
                
            posiciones_sup.insert(cercano, falta)
            ya_ingresados.add(falta)
            correlaciones.pop(0)
            i = 0
            
            if cercano == 0:
                posiciones_inf.insert(cercano,-1)

            else:
                # Se agregó el producto al final o se remplazo por un -1
                continue

    return

def escribir_simuladas(n, tickets):
    boletas = crear_n_boletas(n, tickets)

    with open('Boletas Simuladas2.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        for bid in boletas:
            writer.writerow(boletas[bid].products)

    print(chi_cuadrado(boletas))



ventas = leer_datos()


print("VENTAS", ventas)
print("TICKETS", len(all_tickets))
print("PRODUCTOS", len(all_products))
print("ESPACIOS", ESPACIOS)



escribir_simuladas(7347, all_tickets)
#print_graph_simulado(100, all_tickets)
#print_graph_real()


# aparece_x_temporadas()
# fase_1()

# escribir_uso_posiciones()
# analisis_datos()
