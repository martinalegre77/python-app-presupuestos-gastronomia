# Pestaña de gestión de bebidas

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from extras import paths, estilos, funciones
from modelos.models import BebidasMesaModel, BebidasModel, CapacidadMlModel, TragosModel

class BebidasTab:
    def __init__(self, parent, master):

        self.parent = parent  # Referencia al Notebook donde se agregará la pestaña
        self.master = master  # Referencia a la ventana principal
        self.frame = ttk.Frame(self.parent, style=estilos.style_notebook())
        # Obtengo los datos de la DB
        self.bebidas_model = BebidasModel()
        self.bebidas = self.bebidas_model.read_all_ordered_by('nombre')
        self.capacidad_model = CapacidadMlModel()
        self.capacidad_en_ml = self.capacidad_model.read_all()
        self.tragos_model = TragosModel()
        self.bebidas_mesa_model = BebidasMesaModel()

        self.setup_ui()


    def setup_ui(self):
        # Aplicar estilos
        estilos.style_notebook()

        # Configurar el grid de la pestaña
        self.frame.columnconfigure(0, weight=1) # vacía izquierda
        self.frame.columnconfigure(1, weight=0) # izquierda para la lista de bebidas
        self.frame.columnconfigure(2, weight=1) # central para espacio vacío
        self.frame.columnconfigure(3, weight=0) # derecha en mesa
        self.frame.columnconfigure(4, weight=1) # derecha para espacio vacío
        self.frame.rowconfigure(0, weight=0) # Fila para el título
        self.frame.rowconfigure(1, weight=0) # Fila para el contenido principal
        # Titulo de la pestaña
        tk.Label(self.frame, text="BEBIDAS", bg=estilos.TAPIZ, font=("Arial", 16, "bold")).grid(row=0, column=1, columnspan=2, pady=25)

        # Frame principal 
        main_frame = ttk.Frame(self.frame, style="TFrame")
        main_frame.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1) # Columna para la lista de bebidas
        main_frame.columnconfigure(1, weight=1) # Columna para las bebidas en mesa
        main_frame.rowconfigure(0, weight=1) # Fila para la lista de bebidas y bebidas en mesa
        main_frame.rowconfigure(1, weight=0) # Fila para los botones
        
        # Columna 1: Lista de bebidas

        # Frame para la tabla (Treeview + Scrollbar)
        table_frame = ttk.Frame(main_frame, style="TFrame")
        table_frame.grid(row=1, column=1, padx=2, pady=5, sticky='nwe')
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        # Inicializar scrollbar sin command
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=None) 
        # Tabla (Treeview) con Scrollbar
        self.tree = ttk.Treeview(table_frame, columns=("id", "Nombre", "Marca", "Presentación", "Precio", "Proveedor", "Pack x"), 
                                show="headings", 
                                height=10,
                                style="Treeview", 
                                yscrollcommand=scrollbar.set)
        # Configurar el command después de crear el Treeview
        scrollbar.config(command=self.tree.yview)
        # Definir las columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Presentación", text="Presentación")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.heading("Pack x", text="Pack x")
        # Ajustar el ancho de las columnas
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("Nombre", width=190, stretch=True)
        self.tree.column("Marca", width=160, stretch=True, anchor=tk.CENTER)
        self.tree.column("Presentación", width=140, stretch=False, anchor=tk.E)
        self.tree.column("Precio", width=100, stretch=True, anchor=tk.E)
        self.tree.column("Proveedor", width=120, stretch=True, anchor=tk.CENTER)
        self.tree.column("Pack x", width=80, stretch=False, anchor=tk.CENTER)
        # Usar grid para el Treeview
        self.tree.grid(row=0, column=0, sticky='nsew') 
        # Usar grid para el Scrollbar, a la derecha
        scrollbar.grid(row=0, column=1, sticky='ns') 
        
        # Llenar la tabla
        self.llenar_tabla()
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.grid(row=2, column=1, pady=20, sticky="ew")  
        
        # Botones dentro del frame
        add_button = ttk.Button(button_frame, text="➕ Agregar Bebida", command=self.agregar_bebida, cursor='hand2', style="Accent.TButton")
        add_button.grid(row=0, column=0, padx=5, sticky="we")
        modify_button = ttk.Button(button_frame, text="✏️ Modificar Bebida", command=self.modificar_bebida, cursor='hand2', style="Accent.TButton")
        modify_button.grid(row=0, column=1, padx=5, sticky="we")
        delete_button = ttk.Button(button_frame, text="❌ Eliminar Bebida", command=self.eliminar_bebida, cursor='hand2', style="Accent.TButton")
        delete_button.grid(row=0, column=2, padx=5, sticky="we")
        
        # Ajustar las columnas del frame
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        # Columna 2: Bebidas en Mesa

        self.bebidas_mesa_frame = ttk.LabelFrame(main_frame, text="Configurar Bebidas en Mesa", padding=10)
        self.bebidas_mesa_frame.grid(row=1, column=3, sticky="nwe", padx=(40, 5), pady=5)

        self.tipos_bebidas_mesa_keys = {
            "Gaseosa Cola": "bebida_coca",
            "Gaseosa Lima-Limón": "bebida_lima_limon",
            "Agua": "agua",
            "Cerveza": "cerveza",
            "Vino Tinto": "vino_tinto",
            "Vino Blanco": "vino_blanco",
            "Brindis": "brindis",
        }

        self.llenar_bebidas_mesa(self.tipos_bebidas_mesa_keys, self.bebidas_mesa_frame)

        # Frame para el boton Guardar Cambios
        button_frame_barra = ttk.Frame(main_frame, style="TFrame")
        button_frame_barra.grid(row=2, column=3, pady=20, sticky="ew")
        button_frame_barra.columnconfigure(0, weight=1)

        add_button_cambios = ttk.Button(button_frame_barra, text="💾 Guardar cambios",
                                        command=lambda: self.guardar_bebidas_mesa(self.bebidas_mesa_frame),
                                        cursor='hand2', style="Accent.TButton", width=25)
        add_button_cambios.grid(row=0, column=0, padx=(50, 10)) 

        # Botón para actualizar base de datos
        self.actualizar_bebidas_button = ttk.Button(self.frame, text="⟳", command=self.actualizar,
                                                    cursor='hand2', style="Accent.TButton")
        self.actualizar_bebidas_button.grid(row=0, column=2, pady=25, padx=15, sticky="ne")


    def llenar_tabla(self):
        # Limpiar la tabla antes de llenarla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Cargar las bebidas
        bebidas = self.bebidas_model.read_all_ordered_by('nombre')
        # Insertar las bebidas en la tabla
        for bebida in bebidas:
            self.tree.insert("", "end", values=(
                bebida['id'],
                f"  {bebida['nombre'].title()}",
                f"{bebida['marca'].title()}",
                f"{bebida['presentacion']} ml      ",
                f"$ {bebida['precio_compra']:.2f}  ",
                f"{bebida['proveedor'].title()}",
                f"{bebida['pack']}"
            ))


    def llenar_bebidas_mesa(self, tipos_bebidas_mesa_keys, bebidas_mesa_frame):
        bebidas_mesa = self.bebidas_mesa_model.read_all()
        bebidas = self.bebidas_model.read_all_ordered_by('nombre')
        
        lista_nombres_bebidas_con_marca = [f"{bebida['nombre'].title()} - {bebida['marca'].title()}" for bebida in bebidas]
        lista_nombres_bebidas_con_marca.append("Ninguna")
        
        configuracion_default = bebidas_mesa[0] if bebidas_mesa else {} 
        
        row_num = 0

        self.comboboxes_bebidas_mesa = {}

        for tipo_bebida_display, clave_config_db in tipos_bebidas_mesa_keys.items(): 
            tk.Label(bebidas_mesa_frame, text=f"{tipo_bebida_display}:", bg=estilos.GRIS_BOTONES,
                    font=("Arial", 10, "bold")).grid(row=row_num, column=0, padx=5, pady=5, sticky="w")

            combobox = ttk.Combobox(bebidas_mesa_frame, values=lista_nombres_bebidas_con_marca,
                                    state="readonly", font=("Arial", 10), width=25)

            # Obtener el ID de la bebida desde la configuración
            id_bebida = configuracion_default.get(clave_config_db)

            # Establecer el valor inicial buscando el nombre por el ID
            if id_bebida is not None and id_bebida != 0:
                # Encontrar la bebida completa (con nombre y marca) usando el ID
                bebida_inicial = next((bebida for bebida in bebidas if bebida["id"] == id_bebida), None)
                if bebida_inicial:
                    nombre_y_marca_inicial = f"{bebida_inicial['nombre'].title()} - {bebida_inicial['marca'].title()}"
                    if nombre_y_marca_inicial in lista_nombres_bebidas_con_marca:
                        combobox.set(nombre_y_marca_inicial)
                    else: # Si por alguna razón no está en la lista 
                        combobox.set("Ninguna")
                else: # Si el ID no corresponde a ninguna bebida, establecer "Ninguna"
                        combobox.set("Ninguna")
            else:
                combobox.set("Ninguna") # Si no hay ID, establecer "Ninguna"

            combobox.grid(row=row_num, column=1, padx=1, pady=5)
            self.comboboxes_bebidas_mesa[clave_config_db] = combobox

            row_num += 1


    def agregar_bebida(self):
        modal = tk.Toplevel(self.frame)
        modal.title("Agregar Bebida")
        window_width = 360
        window_height = 270
        vx, vy = funciones.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(paths.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Crear campos de edición
        tk.Label(modal, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, "")
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(modal, text="Marca").grid(row=1, column=0, padx=10, pady=5)
        marca_entry = tk.Entry(modal)
        marca_entry.insert(0, "")
        marca_entry.grid(row=1, column=1, padx=10, pady=5)

        # Configurar validación
        vcmd = modal.register(funciones.validate_float_input)
        vnum = modal.register(funciones.validate_numeric_input)

        valores_capacidad_en_ml = funciones.valores_capacidad_en_ml(self.capacidad_en_ml)
        tk.Label(modal, text="Presentación - ml").grid(row=2, column=0, padx=10, pady=5)
        presentacion_combobox = ttk.Combobox(modal, values=valores_capacidad_en_ml, state='normal', height=5, validate="key", validatecommand=(vnum, "%P"))
        presentacion_combobox.set(valores_capacidad_en_ml[0])
        presentacion_combobox.grid(row=2, column=1, padx=(18, 5), pady=5)


        tk.Label(modal, text="Precio - $").grid(row=3, column=0, padx=10, pady=5)
        costo_entry = tk.Entry(modal, validate="key", validatecommand=(vcmd, "%P"))
        costo_entry.insert(0, "1.00")
        costo_entry.grid(row=3, column=1, padx=10, pady=5)

        costo_inc_btn = tk.Button(modal, text="+", command=lambda: funciones.increment(costo_entry), width=2)
        costo_inc_btn.grid(row=3, column=2, padx=5, pady=5)
        costo_dec_btn = tk.Button(modal, text="-", command=lambda: funciones.decrement(costo_entry), width=2)
        costo_dec_btn.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(modal, text="Proveedor").grid(row=4, column=0, padx=10, pady=5)
        prov_entry = tk.Entry(modal)
        prov_entry.insert(0, "")
        prov_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(modal, text="Un x Pack").grid(row=5, column=0, padx=10, pady=5)
        pack_entry = tk.Entry(modal, validate="key", validatecommand=(vnum, "%P"))
        pack_entry.insert(0, "1")
        pack_entry.grid(row=5, column=1, padx=10, pady=5)

        pack_inc_btn = tk.Button(modal, text="+", command=lambda: funciones.increment_int(pack_entry), width=2)
        pack_inc_btn.grid(row=5, column=2, padx=5, pady=5)
        pack_dec_btn = tk.Button(modal, text="-", command=lambda: funciones.decrement_int(pack_entry), width=2)
        pack_dec_btn.grid(row=5, column=3, padx=5, pady=5)
        
        # Botón Guardar
        tk.Button(modal, text="Guardar", command=lambda: self.guardar_datos(modal,
                                                                    nombre_entry.get().lower(),
                                                                    marca_entry.get().lower(),
                                                                    presentacion_combobox.get(),
                                                                    costo_entry.get(),
                                                                    prov_entry.get().lower(),
                                                                    pack_entry.get()
                                                                    ), 
                                                                    width=20, 
                                                                    background=estilos.BARRA_TOOLS).grid(row=6, column=1, columnspan=1, pady=20)


    def modificar_bebida(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para modificar.")
            return
        
        # Obtener el ID desde los metadatos del TreeView
        selected_item = selected_item[0]
        id_item = self.tree.set(selected_item, 'id')
        if not id_item:
            messagebox.showerror("Error", "No se encontró la bebida seleccionada.")
            return
        
        # Obtener datos de la base de datos usando el ID
        bebida = self.bebidas_model.read_by_id(int(id_item))
        if not bebida:
            messagebox.showerror("Error", "No se pudo encontrar la bebida en la base de datos.")
            return

        # Ventana para modificar los valores
        modal = tk.Toplevel(self.frame)
        modal.title("Modificar Bebida")
        window_width = 360
        window_height = 270
        vx, vy = funciones.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(paths.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Crear campos de edición
        tk.Label(modal, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, bebida['nombre'].title())
        nombre_entry.config(state="readonly")
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(modal, text="Marca").grid(row=1, column=0, padx=10, pady=5)
        marca_entry = tk.Entry(modal)
        marca_entry.insert(0, bebida['marca'].title())
        marca_entry.grid(row=1, column=1, padx=10, pady=5)

        valores_capacidad_en_ml = funciones.valores_capacidad_en_ml(self.capacidad_en_ml)
        tk.Label(modal, text="Presentación - ml").grid(row=2, column=0, padx=10, pady=5)
        presentacion_combobox = ttk.Combobox(modal, values=valores_capacidad_en_ml, state='readonly', height=5)
        presentacion_combobox.set(bebida['presentacion'])
        presentacion_combobox.grid(row=2, column=1, padx=(15, 5), pady=5)

        # Configurar validación
        vcmd = modal.register(funciones.validate_float_input)
        vnum = modal.register(funciones.validate_numeric_input)

        tk.Label(modal, text="Precio - $").grid(row=3, column=0, padx=10, pady=5)
        costo_entry = tk.Entry(modal, validate="key", validatecommand=(vcmd, "%P"))
        costo_entry.insert(0, f"{bebida['precio_compra']:.2f}")
        costo_entry.grid(row=3, column=1, padx=10, pady=5)

        costo_inc_btn = tk.Button(modal, text="+", command=lambda: funciones.increment(costo_entry), width=2)
        costo_inc_btn.grid(row=3, column=2, padx=5, pady=5)
        costo_dec_btn = tk.Button(modal, text="-", command=lambda: funciones.decrement(costo_entry), width=2)
        costo_dec_btn.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(modal, text="Proveedor").grid(row=4, column=0, padx=10, pady=5)
        prov_entry = tk.Entry(modal)
        prov_entry.insert(0, bebida['proveedor'].title())
        prov_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(modal, text="Un x Pack").grid(row=5, column=0, padx=10, pady=5)
        pack_entry = tk.Entry(modal, validate="key", validatecommand=(vnum, "%P"))
        pack_entry.insert(0, bebida['pack'])
        pack_entry.grid(row=5, column=1, padx=10, pady=5)

        pack_inc_btn = tk.Button(modal, text="+", command=lambda: funciones.increment_int(pack_entry), width=2)
        pack_inc_btn.grid(row=5, column=2, padx=5, pady=5)
        pack_dec_btn = tk.Button(modal, text="-", command=lambda: funciones.decrement_int(pack_entry), width=2)
        pack_dec_btn.grid(row=5, column=3, padx=5, pady=5)
        
        # Botón Guardar cambios
        tk.Button(modal, text="Guardar", command=lambda: self.guardar_datos(modal, 
                                                                    bebida['nombre'],
                                                                    marca_entry.get().lower(),
                                                                    presentacion_combobox.get(),
                                                                    costo_entry.get(),
                                                                    prov_entry.get().lower(),
                                                                    pack_entry.get(),
                                                                    id_item),
                                                                    width=20, 
                                                                    background=estilos.BARRA_TOOLS).grid(row=6, column=1, columnspan=1, pady=20)


    def eliminar_bebida(self):
        selected_item = self.tree.selection()
        # Comprobar si hay un trago seleccionado
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para eliminar.")
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()
            return
        
        try:
            # Obtener el ID desde los metadatos del TreeView
            selected_item = selected_item[0]
            # Obtener valores
            item_values = self.tree.item(selected_item, 'values')
            id_item = item_values[0]
            nombre_bebida_eliminar = item_values[1]

            # Comprobar que la bebida no sea parte de las bebidas en mesa
            bebida_en_uso = self.verificar_bebida_en_mesa(id_item)
            if bebida_en_uso:
                mensaje = f"La bebida '{nombre_bebida_eliminar.lstrip()}' no se puede eliminar porque está siendo utilizada en las Bebidas en Mesa"
                messagebox.showerror("No se puede eliminar", mensaje)
                return
            
            # Comprobar que la bebida no sea usada en algun trago
            tragos_en_uso = self.verificar_bebida_en_trago(id_item)
            if tragos_en_uso:
                mensaje = f"La bebida '{nombre_bebida_eliminar.lstrip()}' no se puede eliminar porque está siendo utilizada en los siguientes tragos:\n\n"
                mensaje += "\n".join(tragos_en_uso)
                messagebox.showerror("No se puede eliminar", mensaje)
                return
            
            # Si la bebida no está en uso, proceder con la eliminación
            confirm = messagebox.askyesno("Eliminar Bebida", "¿Estás seguro de que deseas eliminar esta bebida?")
            if confirm:
                self.bebidas_model.delete(int(id_item))
                
                # Minimizar la ventana principal
                messagebox.showinfo("Eliminado", "La bebida ha sido eliminada correctamente.")
                
                # Devolver el foco a la pestaña de bebidas
                self.frame.focus_force()
                
                # Actualizar en el TreeView
                for row in self.tree.get_children():
                    self.tree.delete(row)
                
                # Llenar la tabla
                self.llenar_tabla()
                self.llenar_bebidas_mesa(self.tipos_bebidas_mesa_keys, self.bebidas_mesa_frame)
        except ValueError:
            messagebox.showerror("Error", "La bebida no se pudo eliminar.")


    def guardar_datos(self, modal, nombre, marca, presentacion, precio, proveedor, pack, id_item=0):
        if not nombre or not presentacion or not precio or not pack:
            messagebox.showerror("Error", "Los campos 'Nombre', 'Presentación', 'Precio' y 'Pack' deben completarse")
            self.frame.focus_force()
            return

        nueva_bebida = {
                        'nombre': nombre,
                        'marca': marca if marca else "sin marca",
                        'presentacion': int(presentacion),
                        'precio_compra': float(precio),
                        'proveedor': proveedor,
                        'pack': int(pack)
                    }
        try:
            if id_item:
                self.bebidas_model.update(int(id_item), nueva_bebida)
                modal.destroy()
                messagebox.showinfo("Éxito", "Bebida modificada correctamente.")
            else:
                self.bebidas_model.create(nueva_bebida)
                modal.destroy()
                messagebox.showinfo("Éxito", "Bebida agregada correctamente.")
            
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()
            
            # Actualizar en el TreeView
            for row in self.tree.get_children():
                self.tree.delete(row)
            # Llenar la tabla
            self.llenar_tabla()
            self.llenar_bebidas_mesa(self.tipos_bebidas_mesa_keys, self.bebidas_mesa_frame)
        
        except ValueError:
            messagebox.showerror("Error", "Los valores de Costo y Venta deben ser números válidos.")


    def verificar_bebida_en_trago(self, bebida_id_eliminar):
        tragos = self.tragos_model.read_all() # Obtener todos los tragos
        tragos_en_uso = []
        for trago in tragos:
            if 'ingredientes' in trago:
                for ingrediente in trago['ingredientes']:
                    if 'elemento_id' in ingrediente and ingrediente['elemento_id'] == int(bebida_id_eliminar) and ingrediente['tipo'] == "bebida":
                        tragos_en_uso.append(trago['nombre'].title())
                        break # Si se encuentra la bebida en un trago
        return tragos_en_uso
    

    def verificar_bebida_en_mesa(self, bebida_id):
        bebidas = self.bebidas_mesa_model.read_all() 
        for clave, valor in bebidas[0].items():
            if clave != "id":
                if valor == int(bebida_id):
                    return True
        return False
    

    def guardar_bebidas_mesa(self, bebidas_mesa_frame):
        bebidas = self.bebidas_model.read_all_ordered_by('nombre')
        confirm = messagebox.askyesno("Actualizar Bebidas en Mesas", "¿Estás seguro de que deseas realizar modificaciones?")
        if confirm:
            try:
                # Recuperar datos
                bebidas_seleccionadas_ids = {}

                # Iterar sobre el diccionario de Comboboxes que creaste en llenar_bebidas_mesa
                for clave_config_db, combobox_widget in self.comboboxes_bebidas_mesa.items():
                    nombre_y_marca_seleccionado = combobox_widget.get()

                    if nombre_y_marca_seleccionado == "Ninguna":
                        bebidas_seleccionadas_ids[clave_config_db] = 0
                    else:
                        # Separar el nombre y la marca para buscar
                        partes = nombre_y_marca_seleccionado.split(' - ')
                        nombre_busqueda = partes[0].title() 
                        marca_busqueda = partes[1].title() if len(partes) > 1 else None
                        # Buscar el ID de la bebida en self.bebidas 
                        bebida_encontrada = next((bebida for bebida in bebidas if bebida['nombre'].title() == nombre_busqueda and 
                                                    bebida['marca'].title() == marca_busqueda), 
                                                    None)
                                
                        if bebida_encontrada:
                            bebidas_seleccionadas_ids[clave_config_db] = bebida_encontrada['id']
                        else:
                            bebidas_seleccionadas_ids[clave_config_db] = 0 # Si no se encuentra, se guarda como 0 (Ninguna)

                # Guardar los IDs de las bebidas seleccionadas en la base de datos
                self.bebidas_mesa_model.update(1, bebidas_seleccionadas_ids)

                messagebox.showinfo("Bebidas en Mesa", "Bebidas en Mesa modificada exitosamente.")
                self.llenar_bebidas_mesa(self.tipos_bebidas_mesa_keys, self.bebidas_mesa_frame)

            except ValueError:
                messagebox.showerror("Error", "No se pudo modificar Bebidas en Mesa.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado al guardar: {e}")



    def actualizar(self):
        self.llenar_bebidas_mesa(self.tipos_bebidas_mesa_keys, self.bebidas_mesa_frame)
        self.llenar_tabla()
