from model import *

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

def load_supermercado(dict_posiciones, boletas):
    '''
    Función que recibe un diccionario de posiciones sacado en 'load_dict' más una lista de boletas y carga
    un supermercado vacío con las boletas de la lista 'boletas' según la seignación en 'dict_posiciones'.
    '''
    
    return 
