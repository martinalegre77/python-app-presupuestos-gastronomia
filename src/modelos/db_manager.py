# BASES DE DATOS

import os
from pathlib import Path
import sys 
from tinydb import TinyDB, Query

from extras.paths import DATABASE_DIR

# Creación de instancias de TinyDB

# Bebidas
db_bebidas = TinyDB(DATABASE_DIR / 'bebidas.json')
db_tragos = TinyDB(DATABASE_DIR / 'tragos.json')
db_extras_tragos = TinyDB(DATABASE_DIR / 'extras_tragos.json')
db_extras_evento = TinyDB(DATABASE_DIR / 'extras_evento.json')
db_barra_basica = TinyDB(DATABASE_DIR / 'barra_basica.json')
db_bebidas_mesa = TinyDB(DATABASE_DIR / 'bebidas_mesa.json')

# Postres
db_ingredientes = TinyDB(DATABASE_DIR / 'ingredientes.json')
db_insumos = TinyDB(DATABASE_DIR / 'insumos.json')
db_recetas = TinyDB(DATABASE_DIR / 'recetas.json')
db_masa_basica = TinyDB(DATABASE_DIR / 'masa_basica.json')

# contador
db_counters = TinyDB(DATABASE_DIR / 'counters.json') 

# unidades de medida
db_capacidad_en_ml = TinyDB(DATABASE_DIR / 'capacidad_en_ml.json') # bebidas
db_capacidad_en_gr = TinyDB(DATABASE_DIR / 'capacidad_en_gr.json') # insumos
db_cantidad_unidad = TinyDB(DATABASE_DIR / 'cantidad_unidad.json') # ej huevos


# Inicializador de contadores
def initialize_counters():
    """Inicializa contadores para tablas si no existen."""
    for table in ['bebidas', 'tragos', 'ingredientes', 'insumos', 'recetas', "capacidad_en_ml", "capacidad_en_gr", 
                    "cantidad_unidad", "barra_basica", "extras_tragos", "extras_evento", "masa_basica"]:
        if not db_counters.search(Query().table == table):
            db_counters.insert({"table": table, "last_id": 0})


# Obtención del próximo ID autoincremental
def get_next_id(table_name):
    """Obtiene el próximo ID para una tabla específica."""
    result = db_counters.get(Query().table == table_name)
    if result:
        next_id = result['last_id'] + 1
        db_counters.update({'last_id': next_id}, Query().table == table_name)
        return next_id
    return 1


def get_db_instance(table_name):
    """Devuelve la instancia correcta de la base de datos."""
    db_map = {
        "bebidas": db_bebidas,
        "tragos": db_tragos,
        "extras_tragos": db_extras_tragos,
        "extras_evento": db_extras_evento,
        "ingredientes": db_ingredientes,
        "insumos": db_insumos,
        "recetas": db_recetas,
        "masa_basica": db_masa_basica,
        "capacidad_en_ml": db_capacidad_en_ml,
        "capacidad_en_gr": db_capacidad_en_gr,
        "cantidad_unidad": db_cantidad_unidad,
        "barra_basica": db_barra_basica,
        "bebidas_mesa": db_bebidas_mesa
    }
    return db_map.get(table_name)


# Carga de datos por default

def initialize_databases():
    # bebidas
    if len(db_bebidas) == 0:
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "coca cola", "marca": "coca cola", "presentacion": 2250, "precio_compra": 18899.4, "proveedor": "buraglia", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "fernet", "marca": "branca", "presentacion": 750, "precio_compra": 74399.4, "proveedor": "maxiconsumo", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "sprite", "marca": "sprite", "presentacion": 2250, "precio_compra": 18899.4, "proveedor": "dia", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "gancia", "marca": "americano gancia", "presentacion": 950, "precio_compra": 5823.88, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "gin", "marca": "brighton", "presentacion": 700, "precio_compra": 7279.89, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "agua tónica", "marca": "paso de los toros", "presentacion": 1500, "precio_compra": 8099.4, "proveedor": "buraglia", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "ron", "marca": "new style blanco", "presentacion": 1000, "precio_compra": 3359.88, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "campari", "marca": "campari", "presentacion": 750, "precio_compra": 8622.77, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "jugo de naranja", "marca": "cepita", "presentacion": 1000, "precio_compra": 1679.89, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "agua mineral", "marca": "villa del sur", "presentacion": 2250, "precio_compra": 8099.4, "proveedor": "buraglia", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "cerveza", "marca": "artesanal", "presentacion": 20000, "precio_compra": 40000.0, "proveedor": "beer", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "malbec", "marca": "trapiche", "presentacion": 750, "precio_compra": 40799.4, "proveedor": "maxiconsumo", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "sauvignon blanc", "marca": "portillo ", "presentacion": 750, "precio_compra": 21599.4, "proveedor": "maxiconsumo", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "sidra", "marca": "del valle", "presentacion": 700, "precio_compra": 10199.4, "proveedor": "buraglia", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "champagne", "marca": "fresita", "presentacion": 750, "precio_compra": 35999.46, "proveedor": "maxiconsumo", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "chanpagne dulce", "marca": "federico de alvear", "presentacion": 750, "precio_compra": 23999.4, "proveedor": "maxiconsumo", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "champagne extra brut", "marca": "federico de alvear", "presentacion": 750, "precio_compra": 23999.4, "proveedor": "maxiconsumo", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "vermouth", "marca": "cinzano osso", "presentacion": 950, "precio_compra": 6159.89, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "gin ", "marca": "gordon's", "presentacion": 700, "precio_compra": 12879.89, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "jugo de limon", "marca": "marolio", "presentacion": 1000, "precio_compra": 10199.34, "proveedor": "dia", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "jugo de durazno", "marca": "cepita", "presentacion": 1000, "precio_compra": 9899.4, "proveedor": "dia", "pack": 6})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "vodka", "marca": "smirnoff", "presentacion": 700, "precio_compra": 7503.88, "proveedor": "maxiconsumo", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "cachaca ", "marca": "velho barreiro", "presentacion": 900, "precio_compra": 10500.0, "proveedor": "carrefour", "pack": 1})
        db_bebidas.insert({"id": get_next_id("bebidas"), "nombre": "granadina", "marca": "cousenier", "presentacion": 750, "precio_compra": 3583.88, "proveedor": "maxiconsumo", "pack": 1})
        
    # extras de tragos
    if len(db_extras_tragos) == 0:
        db_extras_tragos.insert({"id": get_next_id("extras_tragos"), "nombre": "pulpa de frutilla", "marca": "bahia", "cantidad": 900, "uni_med": "gr", "precio": 3523.38, "proveedor": "maxiconsumo"})
        db_extras_tragos.insert({"id": get_next_id("extras_tragos"), "nombre": "pulpa de durazno", "marca": "bahia", "cantidad": 900, "uni_med": "gr", "precio": 3333.66, "proveedor": "maxiconsumo"})
        db_extras_tragos.insert({"id": get_next_id("extras_tragos"), "nombre": "pulpa de ananá", "marca": "bahia", "cantidad": 900, "uni_med": "gr", "precio": 3523.38, "proveedor": "maxiconsumo"})
        db_extras_tragos.insert({"id": get_next_id("extras_tragos"), "nombre": "azucar", "marca": "ledesma", "cantidad": 1000, "uni_med": "gr", "precio": 1097.48, "proveedor": "vea"})
    
    # extras de evento
    if len(db_extras_evento) == 0:
            db_extras_evento.insert({"id": get_next_id("extras"), "nombre": "hielo", "marca": "ledesma", "precio": 1000, "unidades": 1, "invitados": 10})
            db_extras_evento.insert({"id": get_next_id("extras"), "nombre": "vasos", "marca": "rolito", "precio": 1000, "unidades": 2, "invitados": 1})
            db_extras_evento.insert({"id": get_next_id("extras"), "nombre": "copones", "marca": "pindapoy", "precio": 1000, "unidades": 4, "invitados": 1})
            db_extras_evento.insert({"id": get_next_id("extras"), "nombre": "bartenders", "marca": "pindapoy", "precio": 1000, "unidades": 1, "invitados": 40})
            db_extras_evento.insert({"id": get_next_id("extras"), "nombre": "alquiler barra", "marca": "pindapoy", "precio": 1000, "unidades": 1, "invitados": 10})

    # inicializar bebidas en mesa
    if len(db_bebidas_mesa) == 0:
            db_bebidas_mesa.insert({"id": 1,
                                    "bebida_coca": 0,
                                    "bebida_lima_limon": 0,
                                    "agua": 0,
                                    "cerveza": 0,
                                    "vino_tinto": 0,
                                    "vino_blanco": 0,
                                    "brindis": 0
                                    })


# Postres 

    if len(db_ingredientes) == 0:
        db_ingredientes.insert({"id": get_next_id("ingredientes"), "nombre": "azúcar", "marca": "ledesma", "cantidad": 1000, "uni_med": "gr", "precio": 1097.48, "proveedor": "dia"})
        db_ingredientes.insert({"id": get_next_id("ingredientes"), "nombre": "café", "marca": "morenita", "cantidad": 170, "uni_med": "gr", "precio": 7700, "proveedor": "vea"})
        db_ingredientes.insert({"id": get_next_id("ingredientes"), "nombre": "chocolate semiamargo", "marca": "águila", "cantidad": 1000, "uni_med": "gr", "precio": 16000, "proveedor": "aguaí"})
        db_ingredientes.insert({"id": get_next_id("ingredientes"), "nombre": "chocolate kinder", "marca": "kinder", "cantidad": 100, "uni_med": "gr", "precio": 3900, "proveedor": "vea"})
        db_ingredientes.insert({"id": get_next_id("ingredientes"), "nombre": "crema", "marca": "ramolac", "cantidad": 5000, "uni_med": "gr", "precio": 39200, "proveedor": "carrefour"})

    if len(db_insumos) == 0:
        pass

# Otros
    if len(db_capacidad_en_ml) == 0:
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 250})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 500})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 700})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 750})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 900})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 950})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 1000})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 1125})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 1500})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 2000})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 2250})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 2500})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 3000})
        db_capacidad_en_ml.insert({"id": get_next_id("capacidad_en_ml"), "ml": 20000})


# Inicializar contadores si están vacíos
initialize_counters()

# Inicializar tablas si están vacías
initialize_databases()
