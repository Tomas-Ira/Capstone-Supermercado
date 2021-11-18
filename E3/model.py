import statistics as stat
import seaborn as sns
import numpy as np
from scipy.stats import kurtosis
from Reader import *

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
        self.dict_distacia = dict()
        self.prom_distancia = 0
        self.moda = 0
        self.mediana = 0
        self.curtosis = 0
        self.desv = 0

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

    def poblar_fase_0_permanente(self, productos):
        for i in range(15):
            pasillo = Pasillo(i+1)
            if i < 12:
                zonas = 17
            else:
                zonas = 8
            for j in range(zonas):
                zona = Zona(j+1)
                pasillo.zonas.append(zona)
            self.pasillos.append(pasillo)

        zonas = []
        for p in self.pasillos:
            for z in p.zonas:
                zonas.append(z)

        for n in range(25):
            for zona in zonas:
                producto = productos.pop(0)
                zona.productos.append(producto)
            for i in range(len(zonas)):
                producto = productos.pop(0)
                zona = zonas[228 - i - 1]
                zona.productos.append(producto)

        productos_zona = []
        for pasillo in self.pasillos:
            for zona in pasillo.zonas:
                zona.calcular_demanda()
                productos_zona.append(len(zona.productos))
            pasillo.calcular_demanda()
        #print(productos_zona)
        #print(len(productos_zona))

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

    def generar_heatmap_estacional(self):
        filas = []
        for i in range(17):
            columnas = []
            for j in range(len(self.pasillos)):
                if i < 8:
                    demanda_zona = self.pasillos[j].zonas[i].demanda
                    columnas.append(demanda_zona)
                else:
                    if j < 12:
                        demanda_zona = self.pasillos[j].zonas[i].demanda
                        columnas.append(demanda_zona)
                    else:
                        columnas.append(0)
            filas.append(columnas)
        return filas

    def generar_heatmap_estacional_stdev(self):
        filas = []
        for i in range(17):
            columnas = []
            for j in range(len(self.pasillos)):
                if i < 8:
                    productos = []
                    for p in self.pasillos[j].zonas[i].productos:
                        productos.append(int(p[1]))
                    stdev_zona = int(stat.stdev(productos))
                    columnas.append(stdev_zona)
                else:
                    if j < 12:
                        productos = []
                        for p in self.pasillos[j].zonas[i].productos:
                            productos.append(int(p[1]))
                        stdev_zona = int(stat.stdev(productos))
                        columnas.append(stdev_zona)
                    else:
                        columnas.append(0)
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

    def stdev_por_seccion(self):
        demandas = []
        for p in self.pasillos:
            for z in p.zonas:
                demandas.append(z.demanda)
        return int(stat.stdev(demandas))

    def stdev_por_seccion_estacional(self):
        demandas = []
        for p in self.pasillos:
            for z in p.zonas:
                demandas.append(z.demanda)
        return int(stat.stdev(demandas))

    def stdev_por_pasillo(self):
        demandas = []
        for p in self.pasillos:
            suma_1 = 0
            suma_2 = 0
            contador = 1
            for z in p.zonas:
                if contador <= 8:
                    suma_1 += z.demanda
                else:
                    suma_2 += z.demanda
                contador += 1
            demandas.append(suma_1)
            demandas.append(suma_2)
        return int(stat.stdev(demandas))

    def stdev_por_pasillo_estacional(self):
        demandas = []
        for p in self.pasillos:
            suma_1 = 0
            suma_2 = 0
            contador = 1
            for z in p.zonas:
                if contador <= 8:
                    suma_1 += z.demanda
                else:
                    suma_2 += z.demanda
                contador += 1
            demandas.append(suma_1)
            if suma_2 > 0:
                demandas.append(suma_2)
        return int(stat.stdev(demandas))

    def promedio_stdev_por_seccion(self):
        desviaciones = []
        for p in self.pasillos:
            for z in p.zonas:
                demandas_productos = []
                for p in z.productos:
                    demandas_productos.append(int(p[1]))
                desviaciones.append(stat.stdev(demandas_productos))
        return int(stat.mean(desviaciones))

    def promedio_stdev_por_seccion_estacional(self):
        desviaciones = []
        for p in self.pasillos:
            for z in p.zonas:
                demandas_productos = []
                for p in z.productos:
                    demandas_productos.append(int(p[1]))
                desviaciones.append(stat.stdev(demandas_productos))
        return int(stat.mean(desviaciones))

    def promedio_stdev_por_pasillo(self):
        desviaciones = []
        for p in self.pasillos:
            demandas_pasillo_superior = []
            demandas_pasillo_inferior = []
            contador = 1
            for z in p.zonas:
                if contador <= 8:
                    demandas_pasillo_superior.append(z.demanda)
                else:
                    demandas_pasillo_inferior.append(z.demanda)
                contador += 1
            desviaciones.append(stat.stdev(demandas_pasillo_superior))
            desviaciones.append(stat.stdev(demandas_pasillo_inferior))
        return int(stat.mean(desviaciones))

    def promedio_stdev_por_pasillo_estacional(self):
        desviaciones = []
        for p in self.pasillos:
            demandas_pasillo_superior = []
            demandas_pasillo_inferior = []
            contador = 1
            for z in p.zonas:
                if contador <= 8:
                    demandas_pasillo_superior.append(z.demanda)
                else:
                    demandas_pasillo_inferior.append(z.demanda)
                contador += 1
            desviaciones.append(stat.stdev(demandas_pasillo_superior))
            if len(demandas_pasillo_inferior) > 0:
                desviaciones.append(stat.stdev(demandas_pasillo_inferior))
        return int(stat.mean(desviaciones))

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

    def distribucion_distancias(self, nombre, nro_boletas_muestra = 1000):
        '''
        Función que genera el gráfico de distribución de distancias de un supermercado. Imprime distancias en un archivo de nombre.
        "distancias_recorridas_super_{nombre}.txt".

        * nro_boletas_muestra = cantidad de boletas que considera el gráfico (-1 significa todas).
        * nombre = nombre del supermercado. OJO: no incluir palabra SUPERMERCADO en este nombre.
        
        '''

        # Calculamos distancia recorrida, se imprimen en el archivo 'distancias_recorridas.txt'
        ## Borramos el archivo anterior
        archivo_distancias = f'Archivos Distancias/distancias_recorridas_super_{nombre}.txt'
        with open(archivo_distancias, 'w') as f:
            f.write("DISTANCIAS RECORRIDAS\n")

        boletas = generar_muestra(nro_boletas_muestra)

        _dict_dist, distancias = calcular_distancia(self, nombre, boletas,
         nombre_archivo=archivo_distancias)

        d_f0 = sns.displot(distancias, kde=True)
        tit = f"Distribución de Distancias - Supermercado {nombre}"
        d_f0.set_titles(tit, y=2)
        d_f0.set(xlabel=f"Distancias recorridas", title=tit)

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
    
def calcular_distancia(super, nombre, boletas, nombre_archivo='distancias_recorridas.txt'):
    '''
    Input
    * super
    * nombre -> str con el nombre del supermercado.
    * boletas -> conjunto de boletas.
    * nombre_archivo -> nombre archivo de output, por default 'distancias_recorridas.txt'.

    Output
    * retorna diccionario de las distancias recorridas en cada supermercado, KEYS: {promedio, max, min}.
    * además imprime datos en un archivo de nombre 'nombre_archivo'.
    '''

    with open(nombre_archivo, "a") as f:
        # Se generan los datos
        distancias = [distancia_recorrida(super, x) for x in boletas]
        distancias_clean = [i for i in distancias if i!= 0]
        promedio = int(stat.mean(distancias_clean))
        desv = int(stat.stdev(distancias_clean))
        moda = int(stat.mode(distancias_clean))
        mediana = int(stat.median(distancias_clean))
        #kurtosis = int(kurtosis(distancias_clean))
        dict_datos = {'promedio': promedio, 'max': max(distancias_clean), 'min': min(distancias_clean), 'desv': desv}

        # Guardamos los valores en la clase.
        super.prom_distancia = promedio
        super.moda = moda
        super.mediana = mediana
        super.desv = desv
        # Se escriben en el archivo.
        f.write(" - Supermercado " + nombre + " - \n")
        f.write("\tDistancia promedio: " + str(promedio) + ".\n")
        f.write("\tDesviación estándar: " + str(desv) + ".\n")
        f.write("\tDistancia max: " + str(max(distancias_clean)) + ".\n" )
        f.write("\tDistancia min: " + str(min(distancias_clean)) + ".\n")
        f.write("\n")
    super.dict_distacia = dict_datos
    return dict_datos, distancias_clean
