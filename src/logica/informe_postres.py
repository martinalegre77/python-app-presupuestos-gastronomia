# Confeccion del informe de postres para el empresario

import math
from tkinter import messagebox
from extras.funciones import convertir_pdf, format_name, format_number, formatear_fecha
from extras.paths import APP_INFORMES_PATH, INFORME_POSTRES_PATH_1, INFORME_POSTRES_PATH_2, RECURSOS_DIR
from PIL import Image, ImageDraw, ImageFont
from logica.calculos_postres import calculo_ingredientes_pedido


def imprimir_informe_postres(info_general_pedido, pedido_tartas, pedido_postres, total_venta_general):

    ingredientes_totales_acumulados, detalles_compra_ingredientes, costo_total_ingredientes_estimado, insumos_totales_agrupados, costo_total_insumos_compra = calculo_ingredientes_pedido(pedido_tartas, pedido_postres)

    # Carga del template de fondo
    try:
        lienzo_1 = Image.open(INFORME_POSTRES_PATH_1)
        lienzo_2 = Image.open(INFORME_POSTRES_PATH_2)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al cargar las plantillas: {e}")
        return
    
    # Objeto que usaremos para dibujar sobre el lienzo
    dibujo_1 = ImageDraw.Draw(lienzo_1)
    dibujo_2 = ImageDraw.Draw(lienzo_2)
    
    # Fuentes
    font_regular = ImageFont.truetype(RECURSOS_DIR / 'Montserrat-Regular.ttf', size=28, encoding='utf-8')
    font_regular_30 = ImageFont.truetype(RECURSOS_DIR / 'Montserrat-Regular.ttf', size=30, encoding='utf-8')
    font_header_section = ImageFont.truetype(RECURSOS_DIR / 'Montserrat-Bold.ttf', size=30, encoding='utf-8')
    font_item = ImageFont.truetype(RECURSOS_DIR / 'Montserrat-Regular.ttf', size=22, encoding='utf-8')
    font_total = ImageFont.truetype(RECURSOS_DIR / 'Montserrat-Bold.ttf', size=26, encoding='utf-8')
    font_total_grande = ImageFont.truetype(RECURSOS_DIR / 'Montserrat-Bold.ttf', size=32, encoding='utf-8')

    # Manejo de la posición Y para dibujar
    current_y = 510
    margin_x = 100
    line_height_item = 30
    line_height_section = 50
    line_height_total = 35
    line_height_total_grande = 45

    current_dibujo = dibujo_1
    current_lienzo = lienzo_1
    page_number = 1

    # Función auxiliar para manejar el salto de página
    def check_page_break(y_pos, required_space=line_height_item):
        nonlocal current_y, current_dibujo, current_lienzo, page_number

        if y_pos + required_space > current_lienzo.height - 170: # Ajusta espacio pie de página
            page_number += 1
            if page_number == 2:
                current_dibujo = dibujo_2
                current_lienzo = lienzo_2
                current_y = 220 # Iniciar en la parte superior de la nueva página
            else:
                messagebox.showwarning("Advertencia", "El informe excede el número de páginas predefinido (2). El contenido adicional no se imprimirá.")
                return False
        return True

    # Imprimir datos generales
    # Fecha Hoy
    dibujo_1.text((200, 85), info_general_pedido["fecha_hoy"], font=font_regular, fill='black')
    # Nombre cliente
    if info_general_pedido["telefono_cliente"]:
        dibujo_1.text((225, 339), f"{info_general_pedido['nombre_cliente'].title()} ({info_general_pedido['telefono_cliente']})", font=font_regular_30, fill='black')
    else:
        dibujo_1.text((225, 339), f"{info_general_pedido['nombre_cliente'].title()}", font=font_regular_30, fill='black')
    # Fecha entrega
    dibujo_1.text((355, 407), formatear_fecha(info_general_pedido["fecha_entrega"]), font=font_regular_30, fill='black')

    # DIBUJO DE INGREDIENTES PARA TARTAS Y POSTRES 
    if check_page_break(current_y, line_height_section):
        current_dibujo.text((margin_x, current_y), "DETALLE DE INGREDIENTES REQUERIDOS", font=font_header_section, fill='black')
        current_y += line_height_section

    if not detalles_compra_ingredientes:
        if check_page_break(current_y, line_height_item):
            current_dibujo.text((margin_x + 20, current_y), "No se requiere la compra de ingredientes para este pedido.", font=font_item, fill='black')
            current_y += line_height_item
    else:
        detalles_compra_ingredientes_sorted = sorted(detalles_compra_ingredientes, key=lambda x: x['nombre'])
        for item_compra in detalles_compra_ingredientes_sorted:
            line_text = (f"- {format_name(item_compra['nombre']).title()} - {format_name(item_compra['marca']).title()}."
                        f" Cantidad necesaria: {format_number(item_compra['cantidad_necesaria'])[:-3]} {item_compra['uni_med_necesaria']}. "
                        f"Costo estimado: $ {format_number(item_compra['costo_estimado'])}") 
            if not check_page_break(current_y, line_height_item): 
                break
            
            current_dibujo.text((margin_x + 10, current_y), line_text, font=font_item, fill='black')
            current_y += line_height_item
    
    if check_page_break(current_y, line_height_total):
        current_dibujo.text((margin_x + 30, current_y), f"Costo Total de Ingredientes (Estimado): ${format_number(costo_total_ingredientes_estimado)}", font=font_total, fill='black')
        current_y += line_height_total + 20

    # DIBUJO DE INSUMOS PARA TARTAS Y POSTRES
    if check_page_break(current_y, line_height_section):
        current_dibujo.text((margin_x, current_y), "DETALLE DE INSUMOS REQUERIDOS", font=font_header_section, fill='black')
        current_y += line_height_section

    if not insumos_totales_agrupados:
        if check_page_break(current_y, line_height_item):
            current_dibujo.text((margin_x + 10, current_y), "No se requieren insumos para este pedido.", font=font_item, fill='black')
            current_y += line_height_item
    else:
        insumos_agrupados_sorted = sorted(insumos_totales_agrupados.items(), key=lambda x: x[0][0])
        for (nombre, marca), data in insumos_agrupados_sorted:
            line_text = (f"- {format_name(nombre).title()} - {format_name(marca).title()}. Cantidad necesaria: {data['cantidad_items_usando_insumo']}. "
                            f"Costo Total: $ {format_number(data['costo_total_linea'])}")
            if not check_page_break(current_y, line_height_item): break
            current_dibujo.text((margin_x + 10, current_y), line_text, font=font_item, fill='black')
            current_y += line_height_item

    if check_page_break(current_y, line_height_total):
        current_dibujo.text((margin_x + 30, current_y), f"Costo Total de Insumos: ${format_number(costo_total_insumos_compra)}", font=font_total, fill='black')
        current_y += line_height_total + 20

    # RESUMEN FINAL DEL PEDIDO (COSTO TOTAL DE COMPRA) 
    costo_total_general_compra = costo_total_ingredientes_estimado + costo_total_insumos_compra
    ganancia = total_venta_general - costo_total_general_compra


    if check_page_break(current_y, line_height_section):
        current_dibujo.text((margin_x, current_y), "RESUMEN GENERAL DE COSTOS", font=font_header_section, fill='black')
        current_y += line_height_section

    if check_page_break(current_y, line_height_total):
        current_dibujo.text((margin_x + 30, current_y), f"Costo Total de Ingredientes: ${format_number(costo_total_ingredientes_estimado)}", font=font_total, fill='black')
        current_y += line_height_total
    
    if check_page_break(current_y, line_height_total):
        current_dibujo.text((margin_x + 30, current_y), f"Costo Total de Insumos: ${format_number(costo_total_insumos_compra)}", font=font_total, fill='black')
        current_y += line_height_total + 20
    
    if check_page_break(current_y, line_height_total_grande + 10):
        current_dibujo.text((margin_x, current_y), f"Costo Total General Estimado: ${format_number(costo_total_general_compra)}", font=font_total_grande, fill='black')
        current_y += line_height_total_grande + 10

    if check_page_break(current_y, line_height_total):
        current_dibujo.text((margin_x + 30, current_y), f"Monto Presupuestado: ${format_number(total_venta_general)}", font=font_total, fill='black')
        current_y += line_height_total +20

    if check_page_break(current_y, line_height_total_grande + 10):
        current_dibujo.text((margin_x, current_y), f"Ganancia Bruta: ${format_number(ganancia)}", font=font_total_grande, fill='black')
        current_y += line_height_total_grande + 10    

    # Guardar las imágenes y convertirlas a PDF 
    fecha_formato_archivo = info_general_pedido["fecha_hoy"].replace('/', '-')
    nombre_cliente_formato_archivo = format_name(info_general_pedido["nombre_cliente"]).replace(' ', '_').lower() # Usar format_name y luego reemplazar espacios

    pag1_png_path = APP_INFORMES_PATH / f'informe_compra_postres_{nombre_cliente_formato_archivo}_{fecha_formato_archivo}_pag1.png'
    pag2_png_path = APP_INFORMES_PATH / f'informe_compra_postres_{nombre_cliente_formato_archivo}_{fecha_formato_archivo}_pag2.png'

    # Convertir el informe a PDF y unirlo
    images_to_pdf = []
    png_to_delete = [] 
    
    try:
        # Guardar las páginas como PNG temporales
        lienzo_1.save(pag1_png_path, "PNG")
        png_to_delete.append(pag1_png_path)

        # Cargar la primera imagen como objeto Image 
        img1 = Image.open(pag1_png_path).convert('RGB')
        images_to_pdf.append(img1)

        if page_number > 1: # Solo guardar y agregar la segunda página si se usó
            lienzo_2.save(pag2_png_path, "PNG")
            png_to_delete.append(pag2_png_path)
            
            img2 = Image.open(pag2_png_path).convert('RGB')
            images_to_pdf.append(img2)

        # Llamar a tu función convertir_pdf 
        convertir_pdf(images_to_pdf, 
                        fecha_formato_archivo, 
                        nombre_cliente_formato_archivo, 
                        "informe", 
                        APP_INFORMES_PATH, 
                        png_to_delete)
    except Exception as e:
        messagebox.showerror("Error", f"Error al preparar imagen del informe para PDF: {e}")
        return
