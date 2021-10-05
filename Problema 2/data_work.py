import csv
import sys
import random

print(sys.path[0])
filename = "Problema 2/Popularities.csv"
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

#print(ordenado[:5])
#print(ordenado[-5:])