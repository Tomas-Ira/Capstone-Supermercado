import csv
from random import sample, seed

def leer_datos():
    all_tickets = []
    DATA = [i.strip().split() for i in open("./Data/retail.dat").readlines()]
    for ticket in range(len(DATA)):
        all_tickets.append(DATA[ticket])
    return all_tickets

def leer_datos_simulados(path):
    all_tickets = []
    DATA = [i.strip().split(',') for i in open(path).readlines()]
    for ticket in range(len(DATA)):
        all_tickets.append(DATA[ticket])
    return all_tickets


# Armar muestra
def generar_muestra(n, simulada, path_boletas_simulados="Boletas Simuladas/Boletas Simuladas.csv"):
    if simulada:
        datos_todos = leer_datos_simulados(path_boletas_simulados)
    else:
        datos_todos = leer_datos()
    if n == -1:
        # Usar todas las boletas.
        boletas = datos_todos
    else:
        seed()
        boletas = sample(datos_todos, n)

    return boletas
    