from sys import argv
import pandas as pd
import numpy as np
from collections import defaultdict
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
        self.in_common = defaultdict(int)

    def add_ticket(self, ticket):
        self.tickets.add(ticket)
        self.popularity += 1

    def create_in_common(self):
        for ticket in self.tickets:
            for product in ticket.products:
                if product != self:
                    self.in_common[product.id] += 1
    def show(self):
        print("ID:", self.id, "Popularidad:", self.popularity)
        print("En comun:", self.in_common)


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


def mostrar():
    for id in all_products:
        all_products[id].show()

def armar_relaciones():
    for i in all_products:
        all_products[i].create_in_common()

leer_datos()
armar_relaciones()
mostrar()
