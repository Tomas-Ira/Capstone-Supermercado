from model import *
from collections import defaultdict

def load_dict(supermercado):
    '''
    Función que recibe un supermercado, y retorna un diccionario: {'SKU': 'código_sección'} para todos los 
    productos en el supermercado. En sí, este diccionario representa la asignación SKU -> Zona de un supermercado.
    La idea es que se use este diccionario para cargar un supermercado vacío con boletas. 
    '''
    dict_posiciones = {}
    for pasillo in supermercado.pasillos:
        for zona in pasillo.zonas:
            if zona.id <= 8:
                # Zonas superiores.
                code = f"P{pasillo.id}A-{zona.id}"
            else:
                # Zonas inferiores.
                code = f"P{pasillo.id}B-{zona.id}"
            for producto in zona.set_productos:
                dict_posiciones[producto] = code
    return dict_posiciones

def load_popularities(boletas):
    popularities = defaultdict(int)
    for bol in boletas:
        for sku in bol:
            popularities[int(sku)] += 1
    return popularities

def load_supermercado(dict_posiciones, popularities):
    '''
    Función que recibe un diccionario de posiciones sacado en 'load_dict' y carga
    un supermercado vacío según la asignación de 'dict_posiciones'.
    '''
    # Creamos el supermercado
    supermercado = Supermercado()

    # Lo cargamos
    for i in range(15):
        pasillo = Pasillo(i+1)
        if i < 12:
            zonas = 17
        else:
            zonas = 8
        for j in range(zonas):
            zona = Zona(j+1)
            pasillo.zonas.append(zona)
        supermercado.pasillos.append(pasillo)

    for sku in dict_posiciones.keys():
        indice_pasillo, indice_zona = dict_posiciones[sku].split('-')
        if indice_pasillo[-1] == 'A':
            indice_pasillo = indice_pasillo.replace("A", "")
        else:
            indice_pasillo = indice_pasillo.replace("B", "")
        indice_pasillo = indice_pasillo.replace("P", "")
        
        # Ingresamos [sku, popularidad] en la zona correspondiente
        pas = supermercado.pasillos[int(indice_pasillo) - 1]
        zona = pas.zonas[int(indice_zona) - 1]
        lista_producto = [sku, int(popularities[sku])]
        zona.productos.append(lista_producto)
    
    # Calculamos la demanda en cada zona y pasillo
    for pasillo in supermercado.pasillos:
        for zona in pasillo.zonas:
            zona.calcular_demanda()
        pasillo.calcular_demanda()

    return supermercado
