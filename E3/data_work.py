import csv
import sys
import random

#print('Este es el path: ', sys.path[0])
filename = "./Data/Popularities.csv"
fields = []
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)
#random.seed(8)
#random.shuffle(rows)
ordenados = sorted(rows, key= lambda x: int(x[1]), reverse=True)

#print(ordenados[:5])
#print(ordenados[-5:])