# Logica y computos para calcular el Presupuesto de bebidas

from datetime import datetime
import math
from tkinter import messagebox
from extras.funciones import obtener_fecha_sistema
from logica.imprimir_presupuesto_bebidas import imprimir_presupuesto
from modelos.models import BarraBasicaModel, BebidasMesaModel, BebidasModel, ExtrasTragosModel, TragosModel, ExtrasEventoModel


class PresupuestoCalculador:
    def __init__(self):
        # Instanciar las base de datos
        self.bebidas_model = BebidasModel()
        self.tragos_model = TragosModel()
        self.extras_evento_model = ExtrasEventoModel()
        self.barra_basica_model = BarraBasicaModel()
        self.bebidas_mesa_model = BebidasMesaModel()
        self.extras_tragos_model = ExtrasTragosModel()

        # Consumos por persona de bebidas en mesa (en ML)
        self.CONSUMO_ML_POR_INVITADO = {
                                        "bebida_coca": 700,
                                        "bebida_lima_limon": 300,
                                        "agua": 500,
                                        "cerveza": 330,
                                        "vino_tinto": 270,
                                        "vino_blanco": 70,
                                        "brindis": 250
                                        }


    def calculos_presupuesto(self, nombre_cliente, telefono_cliente, fecha_evento, tipo_evento, cantidad_invitados, 
                            incluye_bebidas, bebidas_en_mesas, lista_barra_basica, lista_tragos_extras):
        
        # Información general del evento 
        info_general_evento = {
            "nombre_cliente": nombre_cliente,
            "telefono_cliente": telefono_cliente,
            "fecha_evento": fecha_evento,
            "tipo_evento": tipo_evento,
            "fecha_hoy": obtener_fecha_sistema(),
            "cantidad_invitados": int(cantidad_invitados),
            "incluye_bebidas": incluye_bebidas 
        }

        num_invitados = int(cantidad_invitados)

        # Acumulador para todos los costos
        acumulador_presupuesto = 0.0


        # CALCULO "BEBIDAS EN MESA"
        # Datos específicos para el cliente sobre bebidas en mesa
        presupuesto_bebidas_mesa = {
            "incluye_bebidas_mesa": False,
            "lista_nombres_bebidas_mesa": [] # Lista de nombres de las bebidas
        }

        # Datos detallados para el informe sobre bebidas en mesa
        informe_bebidas_mesa = {
            "costo_total_bebidas_mesa": 0.0,
            "detalle_bebidas": [] # Lista de diccionarios con todos los detalles de cada bebida
        }
        
        if bebidas_en_mesas:
            try:
                # Consumos totales en ML por tipo de bebida
                consumos_totales_ml = {
                    tipo: consumo_ml * num_invitados
                    for tipo, consumo_ml in self.CONSUMO_ML_POR_INVITADO.items()
                }
                
                # Lectura de bebidas
                all_bebidas_mesa_data = self.bebidas_mesa_model.read_all() 
                config_bebidas_mesa = all_bebidas_mesa_data[0]
                # Actualizar la bandera para el cliente
                presupuesto_bebidas_mesa["incluye_bebidas_mesa"] = True
                # Variable para acumular el costo total de todas las bebidas de mesa
                costo_total_bebidas_mesa_acumulado = 0.0 

                # Unidades necesarias para cada bebida 
                for tipo_bebida_key, bebida_id in config_bebidas_mesa.items():
                    # Omitir id y bebidas con id 0
                    if tipo_bebida_key == 'id' or bebida_id == 0:
                        continue
                    total_ml_para_tipo = consumos_totales_ml.get(tipo_bebida_key, 0)
                    if total_ml_para_tipo > 0:
                        bebida_data = self.bebidas_model.read_by_id(bebida_id)
                        if bebida_data:
                            # Tomo la capacidad por unidad/envase
                            volumen_unitario_ml = bebida_data.get('presentacion', 0)
                            proveedor = bebida_data.get('proveedor', "sin información")
                            if volumen_unitario_ml > 0:
                                unidades_flotantes = total_ml_para_tipo / volumen_unitario_ml
                                unidades_a_comprar = math.ceil(unidades_flotantes)
                                unidades_a_comprar = max(1, unidades_a_comprar)
                                # Calcular cuántos packs necesitamos
                                pack_size = bebida_data.get('pack', 1)
                                num_packs_necesarios = math.ceil(unidades_a_comprar / pack_size)
                                # Calcular las unidades finales ajustadas al pack
                                unidades_finales_pack = num_packs_necesarios * pack_size
                                # Calcular el costo por bebida y acumulación 
                                precio_por_unidad = bebida_data.get('precio_compra', 0.0) 
                                costo_bebida_individual = num_packs_necesarios * precio_por_unidad
                                costo_total_bebidas_mesa_acumulado += costo_bebida_individual
                                # Armar el nombre para luego imprimir
                                if bebida_data.get('nombre').lower() == bebida_data.get('marca').lower():
                                    nombre_bebida_completo = f"{bebida_data.get('nombre').title()}"
                                else:
                                    nombre_bebida_completo = f"{bebida_data.get('nombre').title()} - {bebida_data.get('marca', '').title()}"
                                # Almacenar datos
                                # Para el cliente: solo el nombre de la bebida
                                presupuesto_bebidas_mesa["lista_nombres_bebidas_mesa"].append(nombre_bebida_completo)
                                # Para el empresario: todos los detalles
                                informe_bebidas_mesa["detalle_bebidas"].append({
                                    "nombre": nombre_bebida_completo,
                                    "proveedor": proveedor,
                                    "presentacion": volumen_unitario_ml,
                                    "consumo_total_ml": total_ml_para_tipo,
                                    "unidades_iniciales": unidades_a_comprar,
                                    "pack_size": pack_size,
                                    "packs_a_comprar": num_packs_necesarios,
                                    "unidades_finales_pack": unidades_finales_pack,
                                    "costo_individual": costo_bebida_individual
                                })
                                
                # Asignar el costo total acumulado al informe del empresario
                informe_bebidas_mesa["costo_total_bebidas_mesa"] = costo_total_bebidas_mesa_acumulado

                # Agregar monto de bebidas mesa al acumulador
                acumulador_presupuesto += costo_total_bebidas_mesa_acumulado

            except ValueError:
                messagebox.showerror("Error", "Hubo un error inesperado en el proceso de cálculo.")
                return
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado durante el cálculo de bebidas en mesa: {e}")
                return


        # CALCULO "EXTRAS DE EVENTO" 
        informe_extras_evento_empresario = {
            "costo_total_extras": 0.0,
            "detalle_extras": [] # Lista de diccionarios con los detalles de cada extra
        }

        costo_total_extras_acumulado = 0.0

        try:
            extras_de_evento = self.extras_evento_model.read_all()
            if extras_de_evento:
                for extra_item in extras_de_evento:
                    item_id = extra_item.get('id')
                    nombre_extra = extra_item.get('nombre', 'Desconocido')
                    proveedor = extra_item.get('marca', 'sin información')
                    precio_extra = extra_item.get('precio', 0.0)
                    unidades_extra = extra_item.get('unidades', 1) # Valor por defecto para evitar división por cero
                    invitados_extra = extra_item.get('invitados', 1)

                    # Calcular la cantidad necesaria del item
                    factor_por_unidad = num_invitados / invitados_extra
                    cantidad_necesaria = factor_por_unidad * unidades_extra
                    # Redondeamos hacia arriba para asegurar suficientes items
                    cantidad_necesaria_entera = math.ceil(cantidad_necesaria)

                    # Calcular el costo total por item
                    costo_por_item = cantidad_necesaria_entera * precio_extra
                    costo_total_extras_acumulado += costo_por_item

                    # Almacenar los detalles para el informe del empresario
                    informe_extras_evento_empresario["detalle_extras"].append({
                        "id": item_id,
                        "nombre": nombre_extra,
                        "proveedor": proveedor,
                        "precio_unidad": precio_extra,
                        "unidades_config": unidades_extra,
                        "invitados_config": invitados_extra,
                        "cantidad_necesaria_calculada": cantidad_necesaria_entera,
                        "costo_total_item": costo_por_item
                    })
                    
            informe_extras_evento_empresario["costo_total_extras"] = costo_total_extras_acumulado

            # Agregar monto de extras de evento al acumulador
            acumulador_presupuesto += costo_total_extras_acumulado

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado durante el cálculo de extras de evento: {e}")
            return


        # CALCULO "BARRA DE TRAGOS"
        informe_barra_tragos_empresario = {
            "costo_total_barra": 0.0,
            "detalle_bebidas_barra": [], 
            "detalle_extras_barra": []   
        }
        
        costo_total_barra_acumulado = 0.0

        # Unir ambas listas de tragos
        ids_tragos_seleccionados = list(set(lista_barra_basica + lista_tragos_extras))
        # Diccionarios para acumular las necesidades de ingredientes
        necesidades_ingredientes_barra = {
            "bebidas": {}, # {bebida_id: total_ml_necesarios}
            "extras_tragos": {}   # {extra_id: total_unidades_necesarias}
        }

        try:
            cantidad_tragos_a_hacer = num_invitados * 3 # 3 tragos por invitado

            # Iterar sobre los tragos seleccionados y acumular necesidades de ingredientes
            for trago_id in ids_tragos_seleccionados:
                trago_data = self.tragos_model.read_by_id(trago_id)

                if trago_data:
                    if 'ingredientes' in trago_data and isinstance(trago_data['ingredientes'], list):
                        for ingrediente in trago_data['ingredientes']:
                            ingrediente_id = ingrediente.get('elemento_id')
                            cantidad_por_trago = ingrediente.get('cantidad', 0) 
                            tipo_ingrediente = ingrediente.get('tipo') 

                            if ingrediente_id is None or cantidad_por_trago <= 0 or tipo_ingrediente is None:
                                continue # Si hay algun error con un ingrediente lo saltamos

                            cantidad_total_necesaria_ingrediente = cantidad_por_trago * cantidad_tragos_a_hacer

                            if tipo_ingrediente == 'bebida':
                                if ingrediente_id in necesidades_ingredientes_barra["bebidas"]:
                                    necesidades_ingredientes_barra["bebidas"][ingrediente_id] += cantidad_total_necesaria_ingrediente
                                else:
                                    necesidades_ingredientes_barra["bebidas"][ingrediente_id] = cantidad_total_necesaria_ingrediente
                            elif tipo_ingrediente == 'extra':
                                if ingrediente_id in necesidades_ingredientes_barra["extras_tragos"]:
                                    necesidades_ingredientes_barra["extras_tragos"][ingrediente_id] += cantidad_total_necesaria_ingrediente
                                else:
                                    necesidades_ingredientes_barra["extras_tragos"][ingrediente_id] = cantidad_total_necesaria_ingrediente
            

            # CALCULO COSTO DE BEBIDAS DE LA BARRA
            for bebida_id, total_ml_necesarios in necesidades_ingredientes_barra["bebidas"].items():
                bebida_data = self.bebidas_model.read_by_id(bebida_id)
                if bebida_data:
                    volumen_unitario_ml = bebida_data.get('presentacion', 0)
                    precio_por_unidad = bebida_data.get('precio_compra', 0.0) 
                    pack_size = bebida_data.get('pack', 1)
                    proveedor = bebida_data.get('proveedor', "sin información")

                    if volumen_unitario_ml > 0 and precio_por_unidad > 0 and pack_size > 0:
                        unidades_flotantes = total_ml_necesarios / volumen_unitario_ml
                        unidades_a_comprar = math.ceil(unidades_flotantes)
                        unidades_a_comprar = max(1, unidades_a_comprar) 

                        num_packs_necesarios = math.ceil(unidades_a_comprar / pack_size)
                        unidades_finales_pack = num_packs_necesarios * pack_size
                        
                        costo_bebida_barra = num_packs_necesarios  * precio_por_unidad
                        costo_total_barra_acumulado += costo_bebida_barra

                        # Armar el nombre para luego imprimir
                        if bebida_data.get('nombre').lower() == bebida_data.get('marca').lower():
                            nombre_bebida_completo = f"{bebida_data.get('nombre').title()}"
                        else:
                            nombre_bebida_completo = f"{bebida_data.get('nombre').title()} - {bebida_data.get('marca', '').title()}"
                        
                        informe_barra_tragos_empresario["detalle_bebidas_barra"].append({
                            "id": bebida_id,
                            "nombre": nombre_bebida_completo,
                            "proveedor": proveedor,
                            "consumo_total_ml": total_ml_necesarios,
                            "consumo_total_l": math.ceil(total_ml_necesarios / 1000),
                            "unidades_iniciales": unidades_a_comprar,
                            "pack_size": pack_size,
                            "packs_a_comprar": num_packs_necesarios,
                            "unidades_finales_pack": unidades_finales_pack,
                            "precio_por_unidad": precio_por_unidad,
                            "costo_individual": costo_bebida_barra
                        })
        

            # CALCULO COSTO EXTRAS DE TRAGOS 
            for extra_trago_id, total_unidades_necesarias in necesidades_ingredientes_barra["extras_tragos"].items():
                extra_trago_data = self.extras_tragos_model.read_by_id(extra_trago_id)
                
                if extra_trago_data:
                    volumen_unitario_gr = extra_trago_data.get('cantidad', 0)
                    precio_extra_trago_unidad = extra_trago_data.get('precio', 0.0)
                    proveedor = extra_trago_data.get('proveedor', "sin información")

                    if volumen_unitario_gr > 0 and precio_extra_trago_unidad > 0:
                        unidades_flotantes = total_unidades_necesarias / volumen_unitario_gr
                        unidades_a_comprar = math.ceil(unidades_flotantes)
                        unidades_a_comprar = max(1, unidades_a_comprar)

                        costo_extra_barra = unidades_a_comprar * precio_extra_trago_unidad
                        costo_total_barra_acumulado += costo_extra_barra

                        nombre_extra_trago_completo = f"{extra_trago_data.get('nombre').title()} - {extra_trago_data.get('marca', '').title()}"
                    
                    informe_barra_tragos_empresario["detalle_extras_barra"].append({
                        "id": extra_trago_id,
                        "nombre": nombre_extra_trago_completo,
                        "proveedor": proveedor,
                        "cantidad_necesaria_calculada": unidades_a_comprar,
                        "precio_unidad": precio_extra_trago_unidad,
                        "costo_total_item": costo_extra_barra
                    })
                else:
                    print(f"Advertencia: Extra de trago ID {extra_trago_id} no encontrado en la base de datos de extras de tragos para la barra.")

            informe_barra_tragos_empresario["costo_total_barra"] = costo_total_barra_acumulado

            # Agregar monto de bebidas mesa al acumulador
            acumulador_presupuesto += costo_total_barra_acumulado

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado durante el cálculo de la barra de tragos: {e}")
            return


        # Enviar a imprimir el Presupuesto
        imprimir_presupuesto(info_general_evento, acumulador_presupuesto, informe_bebidas_mesa, presupuesto_bebidas_mesa, 
                                ids_tragos_seleccionados, informe_extras_evento_empresario, necesidades_ingredientes_barra, 
                                informe_barra_tragos_empresario, costo_total_barra_acumulado)



