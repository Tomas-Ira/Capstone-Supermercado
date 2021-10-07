import csv
from random import sample, seed

def leer_datos():
    all_tickets = []
    DATA = [i.strip().split() for i in open("./Data/retail.dat").readlines()]
    for ticket in range(len(DATA)):
        all_tickets.append(DATA[ticket])
    return all_tickets

# Armar muestra
datos_todos = leer_datos()
def generar_muestra(numero):
    seed()
    return sample(datos_todos, numero)
