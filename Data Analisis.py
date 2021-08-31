from sys import argv
import pandas as pd
import numpy as np
import csv

class Ticket:
    def __init__(self, id):
        self.id = id
        self.products = set()

    def add_product(self, product):
        self.products.add(product)
        product.add_ticket(self)

    def has_both(self, prod1, prod2):
        return (prod1 in self.products and prod1 in self.products)

class Product:
    def __init__(self, id):
        self.id = id
        self.tickets = set()
        self.popularity = 0
        self.in_common = {}

    def add_ticket(self, ticket):
        self.tickets.add(ticket)
        self.popularity += 1

    def common(self, other):
        common = 0
        for ticket in self.tickets:
            if ticket.has_both(self, other):
                common += 1
        return common

all_tickets = dict()
all_products = dict()

def leer_datos():
    DATA = [i.strip().split() for i in open("./Data/retail.dat").readlines()]
    for tic in range(len(DATA)):
        new_ticket = Ticket(tic)
        all_tickets[tic] = new_ticket
        for prod in DATA[tic]:
            if prod not in all_products:
                all_products[prod] = Product(prod)
            new_ticket.add_product(all_products[prod])


def obtener_popularidades():
    for id in all_products:
        print("ID:", id, "Popularidad:", all_products[id].popularity)

def armar_relaciones():
    for i in all_products:
        all_products[i]

leer_datos()
obtener_popularidades()
