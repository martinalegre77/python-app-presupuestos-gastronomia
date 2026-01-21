# Funciones CRUD Base de datos

from collections import defaultdict
import operator

from extras import funciones
from .db_manager import get_db_instance, Query, get_next_id

# Querys
class BaseModel:
    def __init__(self, table_name):
        self.db = get_db_instance(table_name)
        self.query = Query()
        self.table_name = table_name
    
    def create(self, data):
        """Crea un nuevo registro con ID autoincremental."""
        data['id'] = get_next_id(self.table_name)  # Obtener el próximo ID autoincremental
        return self.db.insert(data)
    
    def create_all(self, data):
        """Crea un nuevo registro con ID heredado."""
        return self.db.insert(data)
    
    def read_all(self):
        """Obtiene todos los registros."""
        return self.db.all()
    
    def read_by_id(self, record_id):
        """Obtiene un registro por ID."""
        return self.db.get(self.query.id == record_id)
    
    def read_all_ordered_by(self, field_name, reverse=False, case_sensitive=True):
        """
        :param field_name: El nombre del campo por el que ordenar.
        :param reverse: True para ordenar de forma descendente (Z-A, 9-0).
        :param case_sensitive: True para ordenación sensible a mayúsculas/minúsculas.
                                False para ordenación insensible a mayúsculas/minúsculas (convierte a minúsculas).
        """
        records = self.db.all()
        
        if not records: # Si no hay registros, devolver lista vacía
            return []

        # Usar operator.itemgetter para un acceso eficiente al campo
        if case_sensitive:
            return sorted(records, key=operator.itemgetter(field_name), reverse=reverse)
        else:
            return sorted(records, key=lambda x: str(x.get(field_name, '')).lower(), reverse=reverse)
    
    def read_by_name(self, name, brand):  
        """Obtiene un registro por Tipo y Nombre."""  
        return self.db.search((self.query.nombre == name) & (self.query.marca == brand))
    
    def update(self, record_id, updates):
        """Actualiza un registro por ID."""
        return self.db.update(updates, self.query.id == record_id)
    
    def delete(self, record_id):
        """Elimina un registro por ID."""
        return self.db.remove(self.query.id == record_id)
    
    def delete_all(self):
        """Elimina todo el contenido."""
        return self.db.truncate()
    
## BARRA ##

# Modelo Bebidas
class BebidasModel(BaseModel):
    def __init__(self):
        super().__init__('bebidas')

# Modelo Tragos
class TragosModel(BaseModel):
    def __init__(self):
        super().__init__('tragos')

# Modelo Extras para tragos
class ExtrasTragosModel(BaseModel):
    def __init__(self):
        super().__init__('extras_tragos')

# Modelo Extras para evento
class ExtrasEventoModel(BaseModel):
    def __init__(self):
        super().__init__('extras_evento')

# Modelo Barra Basica
class BarraBasicaModel(BaseModel):
    def __init__(self):
        super().__init__('barra_basica')

# Modelo Bebidas en Mesa
class BebidasMesaModel(BaseModel):
    def __init__(self):
        super().__init__('bebidas_mesa')


## POSTRES ##

# Modelo Ingredientes
class IngredientesModel(BaseModel):
    def __init__(self):
        super().__init__('ingredientes')

# Modelo Insumos
class InsumosModel(BaseModel):
    def __init__(self):
        super().__init__('insumos')

    def get_processed_insumos_costs(self):
        """
        Calcula el costo unitario para cada insumo y los agrupa por su campo 'uso'.
        Retorna un diccionario donde las claves son los valores de 'uso' y los valores
        son la suma de los costos unitarios de los insumos con ese 'uso'.
        """
        processed_costs = defaultdict(float)
        insumos = self.read_all() 

        for insumo in insumos:
            nombre = insumo.get('nombre', 'Desconocido')
            cantidad_paquete = insumo.get('cantidad')
            precio_paquete = insumo.get('precio')
            uso = insumo.get('uso', '').lower() 

            # Validar que los campos necesarios existan y sean válidos
            if not isinstance(cantidad_paquete, (int, float)) or cantidad_paquete <= 0:
                # print(f"Advertencia: Cantidad inválida para el insumo '{nombre}'. Saltando.")
                continue
            if not isinstance(precio_paquete, (int, float)) or precio_paquete <= 0:
                # print(f"Advertencia: Precio inválido para el insumo '{nombre}'. Saltando.")
                continue

            costo_por_unidad = 0.0

            costo_por_unidad = precio_paquete / cantidad_paquete 

            # Solo sumar al 'uso'
            if uso in funciones.USO_INSUMOS:
                processed_costs[uso] += costo_por_unidad
            
        return dict(processed_costs) # Convertir a dict regular

# Modelo Recetas
class RecetasModel(BaseModel):
    def __init__(self):
        super().__init__('recetas')

# Modelo Masa Basica
class MasaBasicaModel(BaseModel):
    def __init__(self):
        super().__init__('masa_basica')


## OTROS ##

# Modelo Capacidad en ml
class CapacidadMlModel(BaseModel):
    def __init__(self):
        super().__init__('capacidad_en_ml')

# Modelo Capacidad en gr
class CapacidadGrModel(BaseModel):
    def __init__(self):
        super().__init__('capacidad_en_gr')

# Modelo Cantidad Unidad
class CantidadUnidadModel(BaseModel):
    def __init__(self):
        super().__init__('cantidad_unidad')
