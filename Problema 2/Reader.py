import csv
from random import sample, seed

def leer_datos():
    all_tickets = []
    DATA = [i.strip().split() for i in open("./Data/retail.dat").readlines()]
    for ticket in range(len(DATA)):
        all_tickets.append(DATA[ticket])
    return all_tickets

# Armar muestra
def generar_muestra(numero):
    seed()
    return sample(leer_datos(), numero)
