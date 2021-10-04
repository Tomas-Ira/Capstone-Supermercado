import statistics as stat

def intersect(a, b):
    if len(a) > len(b):
        a, b = b, a   
    for c in a:
        if int(c) in b:
            return True

class Zona:
    def __init__(self, id):
        self.id = id
        self.productos = []
        self.set_productos = set()
        self.demanda = 0

    def __str__(self):
        text = "    Zona #" + str(self.id)
        return text

    def calcular_demanda(self):
        suma = 0
        for p in self.productos:
            suma += int(p[1])
            self.set_productos.add(int(p[0]))
        self.demanda = suma

class Pasillo:
    def __init__(self, id):
        self.id = id
        self.zonas = []
        self.demanda = 0

    def __str__(self):
        text = "Pasillo #" + str(self.id)
        return text

    def calcular_demanda(self):
        suma = 0
        for z in self.zonas:
            suma += int(z.demanda)
        self.demanda = suma

class Supermercado:
    def __init__(self):
        self.pasillos = []
        self.demanda_total = 0

    def poblar(self, productos):
        for i in range(15):
            pasillo = Pasillo(i+1)
            for j in range(17):
                zona = Zona(j+1)
                pasillo.zonas.append(zona)
            self.pasillos.append(pasillo)
        for pasillo in self.pasillos:
            id_pasillo = pasillo.id
            base = 17*(id_pasillo-1)
            for zona in pasillo.zonas:
                id_zona = zona.id + base
                zona.productos = productos[50*(id_zona-1):50*id_zona]
                zona.calcular_demanda() 
            pasillo.calcular_demanda()

    def poblar_fase_0(self, productos):
        for i in range(15):
            pasillo = Pasillo(i+1)
            for j in range(17):
                zona = Zona(j+1)
                pasillo.zonas.append(zona)
            self.pasillos.append(pasillo)
        for n in range(25):
            for pasillo in self.pasillos:
                for zona in pasillo.zonas:
                    producto = productos.pop(0)
                    zona.productos.append(producto)
            for i in range(len(self.pasillos)):
                pasillo = self.pasillos[14 - i]
                for j in range(len(pasillo.zonas)):
                    producto = productos.pop(0)
                    zona = pasillo.zonas[16 - j]
                    zona.productos.append(producto)
        for pasillo in self.pasillos:
            for zona in pasillo.zonas:
                zona.calcular_demanda()
            pasillo.calcular_demanda()

    def calcular_demanda(self):
        suma = 0
        for p in self.pasillos:
            for z in p.zonas:
                suma += z.demanda
        self.demanda_total = suma
        return suma

    def generar_heatmap(self):
        filas = []
        for i in range(17):
            columnas = []
            for p in self.pasillos:
                demanda_zona = p.zonas[i].demanda
                columnas.append(demanda_zona)
            filas.append(columnas)
        return filas

    def match_pasillos(self, lista):
        pasillos_a_visitar = []
        productos = set(lista)
        for p in self.pasillos:
            contador = 0
            for z in p.zonas:
                contador += 1
                if intersect(productos, z.set_productos):
                    if contador <= 8:
                        pasillos_a_visitar.append("P" + str(p.id) + "A")
                    else:
                        pasillos_a_visitar.append("P" + str(p.id) + "B")
        return sorted(list(set(pasillos_a_visitar)))

    def varianza(self):
        demandas = []
        for p in self.pasillos:
            for z in p.zonas:
                demandas.append(z.demanda)
        return int(stat.pvariance(demandas))

    def promedio(self):
        demandas = []
        for p in self.pasillos:
            for z in p.zonas:
                demandas.append(z.demanda)
        return int(stat.mean(demandas))

    def heatmap_pasillos(self):
        demandas = [[], []]
        for p in self.pasillos:
            contador = 0
            suma_a = 0
            suma_b = 0
            for z in p.zonas:
                contador += 1
                if contador <= 8:
                    suma_a += z.demanda
                else:
                    suma_b += z.demanda
            demandas[0].append(suma_a)
            demandas[1].append(suma_b)
        return demandas


def top_5(lista):
    lista_completa = []
    for l in lista:
        for elem in l:
            lista_completa.append(elem)
    lista_completa.sort()
    min_5 = lista_completa[:5]
    max_5 = lista_completa[-5:]
    return min_5[::-1], max_5

def guardar_distribucion(super, mins, maxs, nombre):
    with open(nombre, "w") as f:
        f.write("Distribucion Supermercado - Demanda total: " + str(super.calcular_demanda()) + "\n")
        f.write("Varianza demanda por seccion: " + str(super.varianza()) + "\n")
        f.write("Promedio demanda por seccion: " + str(super.promedio()) + "\n")
        f.write("Mayor demanda en una seccion: " + str(maxs[4]) + "\n")
        f.write("Menor demanda en una seccion: " + str(mins[4]) + "\n")
        f.write("\n")

        for p in super.pasillos:
            f.write("Pasillo " + str(p.id) + " - Demanda del pasillo: " + str(p.demanda) + "\n\n")
            numero_pasillo = "P" + str(p.id)
            for z in p.zonas:
                f.write("   " + numero_pasillo + " - Seccion " + str(z.id) + " - Demanda de la seccion: "+ str(z.demanda) + "\n\n")
                f.write("       Producto | Demanda\n")
                productos = sorted(z.productos, key=lambda x: int(x[1]), reverse=True)
                for p in productos:
                    id_p = str(p[0])
                    demanda = str(p[1])
                    largo_id = len(id_p)
                    extra = (9 - largo_id) * " "
                    f.write("       " + id_p + extra + "| " + demanda + "\n")
                f.write("\n")

def contador_visitas_por_pasillo(super, lista):
    pasillos = {"P1A": 0, 'P2A': 0,'P3A': 0, 'P4A': 0,'P5A': 0,'P6A': 0,'P7A': 0,'P8A': 0,'P9A': 0,'P10A': 0,'P11A': 0,'P12A': 0,
                'P13A': 0,'P14A': 0, 'P15A': 0, "P1B": 0, 'P2B': 0,'P3B': 0, 'P4B': 0,'P5B': 0,'P6B': 0,'P7B': 0,'P8B': 0,'P9B': 0,
                'P10B': 0,'P11B': 0,'P12B': 0, 'P13B': 0,'P14B': 0, 'P15B': 0}
    for boleta in lista:
        visitas = super.match_pasillos(boleta)
        for p in visitas:
            pasillos[p] += 1
    superiores = ['P' + str(x) + 'A' for x in range (1,16)]
    inferiores = ['P' + str(x) + 'B' for x in range (1,16)]
    final = [[], []]
    for p in superiores:
        final[0].append(pasillos[p])
    for p in inferiores:
        final[1].append(pasillos[p])
    return final

def distancia_recorrida(super, boleta):
    pasillos_A = 0
    pasillos_B = 0
    pasillos = super.match_pasillos(boleta)
    if len(pasillos) == 0:
        return 0

    for p in pasillos:
        if 'A' in p:
            pasillos_A += 1
        else:
            pasillos_B += 1

    if pasillos_A % 2 == 0:
        if pasillos_A == 0:
            pasillos_A += 2

        if pasillos_B % 2 != 0:
            pasillos_B += 1

    else:
        pasillos_A += 1
        if pasillos_B % 2 != 0:
            pasillos_B += 1

    distancias = []
    for p in pasillos:
        n = int(p.strip('PAB'))
        distancias.append(n)
    horizontal = max(distancias)

    return (pasillos_A * 40) + (pasillos_B * 45) + (horizontal * 6) - 3
    
