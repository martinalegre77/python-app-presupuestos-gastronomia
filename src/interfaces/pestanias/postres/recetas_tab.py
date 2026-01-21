# Pestaña para gestión de recetas de postres

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from extras import paths, estilos, funciones
from modelos.models import IngredientesModel, MasaBasicaModel, RecetasModel


class RecetasTab:
    def __init__(self, parent, master):
        self.parent = parent  # Referencia al Notebook donde se agregará la pestaña
        self.master = master  # Referencia a la ventana principal
        self.frame = ttk.Frame(self.parent, style=estilos.style_notebook())
        
        # Instanciar modelos (bases de datos)
        self.masa_basica_model = MasaBasicaModel()
        self.ingredientes_model = IngredientesModel()
        self.recetas_model = RecetasModel()
        self.masa_basica = self.masa_basica_model.read_all()
        
        # Confeccionar pestaña
        self.setup_ui()


    def setup_ui(self):
        # Aplicar estilos
        estilos.style_notebook()
        # Configurar el grid de la pestaña
        self.frame.columnconfigure(0, weight=1) # Columna vacía izquierda
        self.frame.columnconfigure(1, weight=0) # izquierda para la lista de postres
        self.frame.columnconfigure(2, weight=1) # Columna central para espacio vacío
        self.frame.columnconfigure(3, weight=0) # Columna para la Masa Básica
        self.frame.columnconfigure(4, weight=1)  # Columna derecha para espacio vacío
        self.frame.rowconfigure(0, weight=0) # Fila para el título
        self.frame.rowconfigure(1, weight=0) # Fila para el contenido principal
        # Titulo de la pestaña
        tk.Label(self.frame, text="RECETAS DE POSTRES", bg=estilos.TAPIZ, font=("Arial", 16, "bold")).grid(row=0, column=1, columnspan=2, pady=25)

        # Frame principal 
        self.main_frame = ttk.Frame(self.frame, style="TFrame")
        self.main_frame.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.main_frame.columnconfigure(0, weight=1) # Columna para la lista de postres
        self.main_frame.columnconfigure(1, weight=1) # Columna para la masa básica
        self.main_frame.rowconfigure(0, weight=1) # Fila para la lista de postres y masa básica (comparten espacio)
        self.main_frame.rowconfigure(1, weight=0) # Fila para los botones 
        
        # Columna 1: Gestión de Postres 
        content_frame = ttk.LabelFrame(self.main_frame, text="Gestión de recetas", padding=10)
        content_frame.grid(row=0, column=1, padx=2, pady=5, sticky='nwe')
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        # Tabla (Treeview) con Scrollbar
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(side='left', padx=10, anchor="n")
        self.tree = ttk.Treeview(table_frame, columns=("id", "Nombre", "Ingredientes", "P.G.", "P.M."), show="headings", height=10, style="Treeview")
        self.tree.heading("id", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Ingredientes", text="Ingredientes")
        self.tree.heading("P.G.", text="P.G.")
        self.tree.heading("P.M.", text="P.M.")
        # Ajustar el ancho de las columnas
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("Nombre", width=220, stretch=True)
        self.tree.column("Ingredientes", width=110, anchor="center")
        self.tree.column("P.G.", width=40, anchor="center")
        self.tree.column("P.M.", width=40, anchor="center")
        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set, style="Treeview")
        self.tree.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')
        # Llenar la tabla con datos
        self.llenar_tabla()
        # Combobox para ingredientes (a la derecha del scrollbar)
        combobox_frame = ttk.Frame(content_frame, style="ComboBoxFrame.TLabelframe")
        combobox_frame.pack(side='left', padx=10, anchor="n")
        tk.Label(combobox_frame, text="Detalle", bg=estilos.GRIS_BOTONES, font=("Arial", 12, "bold")).pack(pady=5)
        self.ingredientes_combobox = ttk.Combobox(combobox_frame, state="readonly", width=40, style="TCombobox")
        self.ingredientes_combobox.pack(pady=10, fill='x')
        self.ingredientes_combobox.set("Seleccione un postre")
        # Botones de acción
        button_frame = ttk.Frame(self.main_frame, style="TFrame")
        button_frame.grid(row=1, column=1, pady=20, sticky="ew")  # Alineación arriba y expandido horizontalmente
        # Ajustar las columnas del frame
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        # Botones dentro del frame
        add_button = ttk.Button(button_frame, text="➕ Agregar Postre", style="Accent.TButton", cursor='hand2', command=self.agregar_postre)
        edit_button = ttk.Button(button_frame, text="✏️ Modificar Postre", style="Accent.TButton", cursor='hand2', command=self.modificar_postre)
        delete_button = ttk.Button(button_frame, text="❌ Eliminar Postre", style="Accent.TButton", cursor='hand2', command=self.borrar_postre)
        add_button.grid(row=0, column=0, padx=10, sticky="ew")
        edit_button.grid(row=0, column=1, padx=10, sticky="ew")
        delete_button.grid(row=0, column=2, padx=10, sticky="ew")

        # Columna 2: Configuración de la Masa Básica 
        masa_basica_frame = ttk.LabelFrame(self.main_frame, text="Configurar Masa Básica", padding=10)
        masa_basica_frame.grid(row=0, column=3, sticky="nwe", padx=(40, 5), pady=5)
        # label para la masa basica
        tk.Label(masa_basica_frame, text="Cantidad de ingredientes:", bg=estilos.GRIS_BOTONES,
                font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        # Combobox para seleccionar la cantidad de ingredientes
        self.cantidad_combobox_masa = ttk.Combobox(masa_basica_frame, values=list(range(1, 11)),
                                                    state="readonly", font=("Arial", 12, "bold"), width=4)
        self.cantidad_combobox_masa.set(len(self.masa_basica)) 
        self.cantidad_combobox_masa.grid(row=0, column=1, padx=1, pady=5)
        # Frame para la lista de ingredientes
        self.masa_frame_ingredientes = ttk.Frame(masa_basica_frame, style="TragosFrame.TFrame")
        self.masa_frame_ingredientes.grid(row=1, column=0, columnspan=2, padx=30, pady=10, sticky="ew") # sticky ew para expandir horizontalmente
        self.cantidad_combobox_masa.bind("<<ComboboxSelected>>", lambda event: self.actualizar_campos_masa_base(event, self.cantidad_combobox_masa))
        self.actualizar_campos_masa_base(None, self.cantidad_combobox_masa)
        # Frame para el boton Guardar Cambios
        button_frame_masa = ttk.Frame(self.main_frame, style="TFrame")
        button_frame_masa.grid(row=1, column=3, pady=20, sticky="ew")
        button_frame_masa.columnconfigure(0, weight=1)
        # Boton para guardar cambios
        add_button_cambios = ttk.Button(button_frame_masa, text="💾 Guardar cambios",
                                        command=lambda: self.guardar_masa_basica(self.masa_frame_ingredientes, self.actualizar_campos_masa_base),
                                        cursor='hand2', style="Accent.TButton", width=25)
        add_button_cambios.grid(row=0, column=0, padx=(50, 10)) 

        # Botón para actualizar base de datos
        self.actualizar_bebidas_button = ttk.Button(self.frame, text="⟳", command=self.actualizar,
                                                    cursor='hand2', style="Accent.TButton")
        self.actualizar_bebidas_button.grid(row=0, column=2, pady=25, padx=15, sticky="ne")


    def _load_all_elements(self): # Función interna para cargar todos los ingredientes
        ingredientes = self.ingredientes_model.read_all()

        self.all_elementos = []

        for ingrediente in ingredientes:
            nombre = ingrediente['nombre'].title()
            medida = ingrediente['uni_med']
            marca_ingrediente = ingrediente.get('marca')
            if marca_ingrediente:
                marca_display = str(marca_ingrediente).title()
                full_nombre = f"{nombre} - {marca_display} - {medida}"
            else:
                marca_display = "s/marca" 
                full_nombre = f"{nombre} - {marca_display} - {medida}" 

            self.all_elementos.append({
                "id": ingrediente['id'],
                "nombre": nombre, 
                "marca": marca_display, 
                "uni_med": medida, 
                "full_nombre": full_nombre 
            })


    def actualizar_campos_masa_base(self, event, cantidad_combobox):
        # Obtener la cantidad seleccionada
        cantidad = int(cantidad_combobox.get())
        # Cargar la lista de los ingredientes de la masa base
        masa_basica = self.masa_basica_model.read_all()
        # Cargar la lista de todos los ingredientes
        ingredientes = self.ingredientes_model.read_all()
        
        ingredientes_list = []
        # Crear un diccionario para mapear el nombre completo a ID y viceversa
        self.ingredientes_full_name_to_id = {}
        self.ingredientes_id_to_full_name = {}
        self.ingredientes_id_to_details = {} # Para las cantidades
        
        for ingrediente in ingredientes:
            nombre = ingrediente.get('nombre', 'N/A').title()
            marca = ingrediente.get('marca')
            if not marca:
                marca = "s/marca"
            else:
                marca = marca.title()
            medida = ingrediente.get('uni_med')
            # Construir el nombre completo que se mostrará en el Combobox
            full_name_display = f"{nombre} - {marca} - {medida}"
            ingredientes_list.append(full_name_display)

            for ing in ingredientes:
                self.ingredientes_full_name_to_id[full_name_display] = ingrediente['id']
                self.ingredientes_id_to_full_name[ingrediente['id']] = full_name_display
                self.ingredientes_id_to_details[ingrediente['id']] = ingrediente # Guarda los detalles completos

        # Pre-cargar las cantidades de la masa básica actual
        masa_basica_precargada = {item['id']: item['cantidad'] for item in masa_basica}

        # Limpiar el contenedor de ingredientes
        for widget in self.masa_frame_ingredientes.winfo_children():
            widget.destroy()

        # Lista para almacenar las referencias a los Combobox y Entries creados
        self.masa_basica_widgets = []

        # Crear campos para la cantidad seleccionada de ingredientes
        for i in range(cantidad):
            tk.Label(self.masa_frame_ingredientes, text=f"Ingrediente {i + 1}", bg=estilos.GRIS_BOTONES).grid(row=i, column=0, padx=5, pady=2, sticky="w")
            
            ingrediente_combobox = ttk.Combobox(self.masa_frame_ingredientes, values=ingredientes_list, state="readonly", width=30, name=f'ingrediente_combobox_{i}', style="Barra.TCombobox")
            ingrediente_combobox.grid(row=i, column=1, padx=5, pady=2, sticky="ew") # sticky ew para expandir horizontalmente
            ingrediente_combobox.set("Ingrediente...")

            # Precargar ingrediente del Combobox
            # Buscar el ID del ingrediente en masa_basica basado en el orden o ID
            if i < len(masa_basica) and masa_basica[i]['id'] in self.ingredientes_id_to_full_name:
                ingrediente_combobox.set(self.ingredientes_id_to_full_name[masa_basica[i]['id']])

            vnum = self.masa_frame_ingredientes.register(funciones.validate_numeric_input)
            
            cantidad_entry = tk.Entry(self.masa_frame_ingredientes, width=7, name=f'cantidad_entry_{i}', validate="key", validatecommand=(vnum, "%P"))
            cantidad_entry.grid(row=i, column=2, padx=5, pady=2)
            cantidad_entry.insert(0, "Cantidad")

            # Precargar cantidad del Entry
            if i < len(masa_basica) and masa_basica[i]['id'] in masa_basica_precargada:
                cantidad_entry.delete(0, tk.END)
                cantidad_entry.insert(0, str(masa_basica_precargada[masa_basica[i]['id']]))
            
            # Guardar la referencia a los widgets en una lista para poder recuperarlos en guardar_masa_basica
            self.masa_basica_widgets.append({
                'combobox': ingrediente_combobox,
                'entry': cantidad_entry
            }) 


    def llenar_tabla(self):
        # Limpiar la tabla antes de llenarla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Cargar los postres
        postres = self.recetas_model.read_all_ordered_by('nombre')
        # Llenar la tabla con los datos
        for receta in postres:
            self.tree.insert("", "end", values=(
                receta['id'],
                f"  {receta['nombre'].title()}",
                receta['cantidad_ingredientes'],
                receta['porc_grande'],
                receta['porc_mini'],
            ))

        def on_tree_selection(event):
            selected_item = self.tree.selection()
            # Para buscar los detalles de los ingredientes y productos
            all_ingredientes = self.ingredientes_model.read_all_ordered_by('nombre')   

            if selected_item:
                item = self.tree.item(selected_item)
                receta_id = item['values'][0]  # Capturar el ID del postre seleccionado
                # Buscar la receta completa 
                receta_completa = self.recetas_model.read_by_id(receta_id)
                
                if receta_completa and 'ingredientes' in receta_completa:
                    ingredientes_list = [] 

                    for ing in receta_completa['ingredientes']:
                        elemento_detalle = None 

                        # Buscar el ingrediente por su ID en la lista de ingredientes
                        elemento_detalle = next((b for b in all_ingredientes if b['id'] == ing['elemento_id']), None)
                        
                        if elemento_detalle:
                            nombre = elemento_detalle.get('nombre', 'Desconocido').title()
                            marca = elemento_detalle.get('marca').title()
                            if marca:
                                ingrediente_str = f"{nombre} - {marca} - {ing['cantidad']} {ing['uni_med']}"
                            else:
                                ingrediente_str = f"{nombre} - {ing['cantidad']} {ing['uni_med']}"
                            ingredientes_list.append(ingrediente_str)

                    if receta_completa['masa_base']:
                        ingredientes_list.append('INCLUYE Masa Básica')
                    else: 
                        ingredientes_list.append('NO INCLUYE Masa Básica')

                    if ingredientes_list:
                        self.ingredientes_combobox['values'] = ingredientes_list
                        self.ingredientes_combobox.set("Despliegue para ver los ingredientes")
                    else:
                        self.ingredientes_combobox['values'] = ["Sin ingredientes"]
                        self.ingredientes_combobox.set("Sin ingredientes")

                else:
                    # Si el postre no tiene la clave 'ingredientes' o está vacía
                    self.ingredientes_combobox['values'] = ["Sin ingredientes"]
                    self.ingredientes_combobox.set("Sin ingredientes")

            else:
                # Si no hay ningún postre seleccionado en el Treeview
                self.ingredientes_combobox['values'] = []
                self.ingredientes_combobox.set("") 

        # Asociar el evento al TreeView
        self.tree.bind("<<TreeviewSelect>>", on_tree_selection)

    
    def agregar_postre(self):
        # Cargar elementos
        self._load_all_elements() 
        # Cargar ventana modal
        modal = tk.Toplevel(self.frame)
        modal.title("Agregar Postre")
        window_width = 430
        window_height = 500
        vx, vy = funciones.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(paths.ICONO_DESSERT)
        modal.focus() 
        modal.grab_set()
        
        # Crear campos de edición
        tk.Label(modal, text="Nombre", bg=estilos.BARRA_TITULO, fg="black").grid(row=0, column=0, padx=10, pady=5, sticky='we')
        nombre_entry = tk.Entry(modal, width=22)
        nombre_entry.insert(0, "")
        nombre_entry.grid(row=0, column=1, padx=30, pady=5, sticky="we")
        tk.Label(modal, text="Cantidad de ingredientes", bg=estilos.BARRA_TITULO, fg="black").grid(row=1, column=0, padx=10, pady=5, sticky='we')
        # Guardar cantidad_combobox como atributo de la clase
        cantidad_combobox = ttk.Combobox(modal, values=list(range(1, 13)), state="readonly")  # Hasta 12 ingredientes
        cantidad_combobox.set("1")
        cantidad_combobox.grid(row=1, column=1, padx=30, pady=5, sticky="we")
        # Ingreso de nro de porciones
        vnum = modal.register(funciones.validate_numeric_input)
        frame_porciones = ttk.Frame(modal, style="ModalFrame.TFrame")
        frame_porciones.grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky='we')
        # Configurar el grid de frame_porciones para que los elementos se centren o distribuyan
        frame_porciones.columnconfigure(0, weight=1) # Columna para el label "Porc. grande"
        frame_porciones.columnconfigure(1, weight=0) # Columna para el entry grande
        frame_porciones.columnconfigure(2, weight=1) # Espacio entre entries
        frame_porciones.columnconfigure(3, weight=0) # Columna para el label "Porc. mini"
        frame_porciones.columnconfigure(4, weight=1) # Columna para el entry mini
        tk.Label(frame_porciones, text="Porc. grande:", bg=estilos.BARRA_TITULO, fg="black").grid(row=0, column=0, padx=(30, 5), pady=5, sticky='e')
        self.grande_entry = tk.Entry(frame_porciones, width=4, validate="key", validatecommand=(vnum, "%P"))
        self.grande_entry.insert(0, "")
        self.grande_entry.grid(row=0, column=1, padx=10, pady=5, sticky='we')
        tk.Label(frame_porciones, text="Porc. mini:", bg=estilos.BARRA_TITULO, fg="black").grid(row=0, column=3, padx=5, pady=5, sticky='we')
        self.mini_entry = tk.Entry(frame_porciones, width=4, validate="key", validatecommand=(vnum, "%P"))
        self.mini_entry.insert(0, "")
        self.mini_entry.grid(row=0, column=4, padx=10, pady=5, sticky='w')
        # Checkbox "Es tarta"
        self.es_tarta_var = tk.BooleanVar()
        chk_es_tarta = ttk.Checkbutton(modal, text="Es Tarta", variable=self.es_tarta_var,
                                                style="Postre.TCheckbutton"
                                                )
        chk_es_tarta.grid(row=3, column=0, pady=5, padx=(45,5))
        # Checkbox "Incluye Masa Básica"
        self.incluye_masa_base_var = tk.BooleanVar()
        chk_incluye_masa_base = ttk.Checkbutton(modal, text="Incluye Masa Básica", variable=self.incluye_masa_base_var,
                                                style="Postre.TCheckbutton"
                                                )
        chk_incluye_masa_base.grid(row=3, column=1, pady=5, padx=(30,10), sticky='we') 
        # Contenedor dinámico para los ingredientes
        ingredientes_frame = ttk.Frame(modal, style="ModalFrame.TFrame")
        ingredientes_frame.grid(row=4, column=0, columnspan=2, padx=30, pady=5)
        

        def update_ingredient_fields(event, cantidad_combobox):
            # Obtener la cantidad seleccionada
            cantidad = int(cantidad_combobox.get())
            # Limpiar el contenedor de ingredientes (Ver si es necesario limpiar esto)
            for widget in ingredientes_frame.winfo_children():
                widget.destroy()
            # Crear campos para la cantidad seleccionada de ingredientes
            for i in range(cantidad):
                tk.Label(ingredientes_frame, text=f"Ingrediente {i + 1}", bg=estilos.BARRA_TOOLS).grid(row=i, column=0, padx=5, pady=2)
                # Elemento
                elemento_combobox = ttk.Combobox(ingredientes_frame, values=[item['full_nombre'] for item in self.all_elementos], state="readonly", width=33, name=f'elemento_combobox_{i}')
                elemento_combobox.grid(row=i, column=1, padx=5, pady=2)
                elemento_combobox.set("Elemento...")
                # Cantidad
                vnum = modal.register(funciones.validate_numeric_input)
                cantidad_entry = tk.Entry(ingredientes_frame, width=6, name=f'cantidad_entry_{i}', validate="key", validatecommand=(vnum, "%P"))
                cantidad_entry.grid(row=i, column=2, padx=5, pady=2)
                cantidad_entry.insert(0, "Cantidad")

        # Asociar evento al ComboBox
        cantidad_combobox.bind("<<ComboboxSelected>>", lambda event: update_ingredient_fields(event, cantidad_combobox))
        # Inicializar con un ingrediente
        update_ingredient_fields(None, cantidad_combobox)
        
        # Botón para guardar el postre
        tk.Button(modal, text="Guardar", 
                    command=lambda: self.guardar_postre(nombre_entry, 
                                                        ingredientes_frame, 
                                                        modal, 
                                                        self.all_elementos, 
                                                        self.grande_entry.get(),
                                                        self.mini_entry.get(),
                                                        self.incluye_masa_base_var.get(),
                                                        self.es_tarta_var.get()
                                                        ), 
                    width=20, background=estilos.BARRA_TOOLS).grid(row=5, column=0, columnspan=2, pady=10)


    def modificar_postre(self):
        # Cargar ingredientes
        self._load_all_elements() 

        # Cargar seleccion
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona un postre para modificar.")
            return

        # Cargar ventana modal
        modal = tk.Toplevel(self.frame)
        modal.title("Modificar Postre")
        window_width = 430
        window_height = 500
        vx, vy = funciones.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(paths.ICONO_DESSERT)
        modal.focus() 
        modal.grab_set()
        
        # Obtener el ID desde los metadatos del TreeView
        selected_item = selected_item[0]
        id_item = self.tree.set(selected_item, 'id')
        if not id_item:
            messagebox.showerror("Error", "No se encontró el postre seleccionado.")
            return
        
        # Obtener datos de la base de datos usando el ID
        postre = self.recetas_model.read_by_id(int(id_item))
        if not postre:
            messagebox.showerror("Error", "No se pudo encontrar el postre en la base de datos.")
            return
        
        tk.Label(modal, text="Nombre", bg=estilos.BARRA_TITULO, fg="black").grid(row=0, column=0, padx=10, pady=5, sticky='we')
        nombre_entry = tk.Entry(modal, width=22)
        nombre_entry.insert(0, postre['nombre'].title())
        nombre_entry.config(state="readonly")
        nombre_entry.grid(row=0, column=1, padx=30, pady=5, sticky="we")
        tk.Label(modal, text="Cantidad de ingredientes", bg=estilos.BARRA_TITULO, fg="black").grid(row=1, column=0, padx=10, pady=5, sticky='we')
        # Guardar cantidad_combobox como atributo de la clase
        cantidad_combobox = ttk.Combobox(modal, values=list(range(1, 13)), state="readonly")  # Hasta 12 ingredientes
        cantidad_combobox.set(postre['cantidad_ingredientes'])
        cantidad_combobox.grid(row=1, column=1, padx=30, pady=5, sticky="we")
        # Ingreso de nro de porciones
        vnum = modal.register(funciones.validate_numeric_input)
        frame_porciones = ttk.Frame(modal, style="ModalFrame.TFrame")
        frame_porciones.grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky='we')
        # Configurar el grid de frame_porciones para que los elementos se centren o distribuyan
        frame_porciones.columnconfigure(0, weight=1) # Columna para el label "Porc. grande"
        frame_porciones.columnconfigure(1, weight=0) # Columna para el entry grande
        frame_porciones.columnconfigure(2, weight=1) # Espacio entre entries
        frame_porciones.columnconfigure(3, weight=0) # Columna para el label "Porc. mini"
        frame_porciones.columnconfigure(4, weight=1) # Columna para el entry mini
        tk.Label(frame_porciones, text="Porc. grande:", bg=estilos.BARRA_TITULO, fg="black").grid(row=0, column=0, padx=(30, 5), pady=5, sticky='e')
        self.grande_entry = tk.Entry(frame_porciones, width=4, validate="key", validatecommand=(vnum, "%P"))
        self.grande_entry.insert(0, postre["porc_grande"])
        self.grande_entry.grid(row=0, column=1, padx=10, pady=5, sticky='we')
        tk.Label(frame_porciones, text="Porc. mini:", bg=estilos.BARRA_TITULO, fg="black").grid(row=0, column=3, padx=5, pady=5, sticky='we')
        self.mini_entry = tk.Entry(frame_porciones, width=4, validate="key", validatecommand=(vnum, "%P"))
        self.mini_entry.insert(0, postre["porc_mini"])
        self.mini_entry.grid(row=0, column=4, padx=10, pady=5, sticky='w')
        # Checkbox "Es tarta"
        self.es_tarta_var = tk.BooleanVar()
        if postre["es_tarta"] and "es_tarta" in postre:
            self.es_tarta_var.set(postre["es_tarta"])
        else:
            self.es_tarta_var.set(False)
        chk_es_tarta = ttk.Checkbutton(modal, text="Es Tarta", variable=self.es_tarta_var,
                                                style="Postre.TCheckbutton"
                                                )
        chk_es_tarta.grid(row=3, column=0, pady=5, padx=(45,5))
        # Checkbox "Incluye Masa Básica"
        self.incluye_masa_base_var = tk.BooleanVar()
        if postre["masa_base"] and "masa_base" in postre:
            self.incluye_masa_base_var.set(postre["masa_base"])
        else:
            self.incluye_masa_base_var.set(False)
        chk_incluye_masa_base = ttk.Checkbutton(modal, text="Incluye Masa Básica", variable=self.incluye_masa_base_var,
                                                style="Postre.TCheckbutton"
                                                )
        chk_incluye_masa_base.grid(row=3, column=1, pady=5, padx=(30,10), sticky='we') 
        # Contenedor dinámico para los ingredientes
        ingredientes_frame = ttk.Frame(modal, style="ModalFrame.TFrame")
        ingredientes_frame.grid(row=4, column=0, columnspan=2, padx=30, pady=5)


        def update_ingredient_fields(event, cantidad_combobox):
            # Obtener la cantidad seleccionada
            cantidad = int(cantidad_combobox.get())
            # Limpiar el contenedor de ingredientes
            for widget in ingredientes_frame.winfo_children():
                widget.destroy()
            
            # Crear campos para la cantidad seleccionada de ingredientes
            for i in range(cantidad):
                tk.Label(ingredientes_frame, text=f"Ingrediente {i + 1}", bg=estilos.BARRA_TOOLS).grid(row=i, column=0, padx=5, pady=2)

                elemento_combobox = ttk.Combobox(ingredientes_frame, values=[item['full_nombre'] for item in self.all_elementos], state="readonly", width=33, name=f'elemento_combobox_{i}')
                elemento_combobox.grid(row=i, column=1, padx=5, pady=2)
                elemento_combobox.set("Ingrediente...")

                vnum = modal.register(funciones.validate_numeric_input)
                cantidad_entry = tk.Entry(ingredientes_frame, width=6, name=f'cantidad_entry_{i}', validate="key", validatecommand=(vnum, "%P"))
                cantidad_entry.grid(row=i, column=2, padx=5, pady=2)
                cantidad_entry.insert(0, "Cantidad")

                # Rellenar con los datos del postre si existen
                if postre['ingredientes'] and i < len(postre['ingredientes']):
                    ingrediente_data = postre['ingredientes'][i]
                    elemento_id = ingrediente_data['elemento_id']

                    # Buscar el ingrediente completo en self.all_elementos
                    ingrediente_para_mostrar = next(
                                                (item for item in self.all_elementos 
                                                if item['id'] == elemento_id),
                                                None
                                                )
                    
                    if ingrediente_para_mostrar:
                        elemento_combobox.set(ingrediente_para_mostrar['full_nombre']) 
                        cantidad_entry.delete(0, tk.END)
                        cantidad_entry.insert(0, ingrediente_data['cantidad'])

        # Asociar evento al ComboBox
        cantidad_combobox.bind("<<ComboboxSelected>>", lambda event: update_ingredient_fields(event, cantidad_combobox))
        
        # Inicializar con un ingrediente
        update_ingredient_fields(None, cantidad_combobox)
        
        # Botón para guardar el trago
        tk.Button(modal, text="Guardar", 
                    command=lambda: self.guardar_postre(nombre_entry, 
                                                        ingredientes_frame, 
                                                        modal, 
                                                        self.all_elementos, 
                                                        self.grande_entry.get(),
                                                        self.mini_entry.get(),
                                                        self.incluye_masa_base_var.get(), 
                                                        self.es_tarta_var.get(),
                                                        id_item), 
                    width=20, background=estilos.BARRA_TOOLS).grid(row=5, column=0, columnspan=2, pady=10)

    
    def guardar_postre(self, nombre_entry, ingredientes_frame, modal, all_elementos, grande, mini, 
                        incluye_masa_base_var, es_tarta_var, id_postre = 0):
        # Guardar datos del postre
        nombre = nombre_entry.get().strip()
        ingredientes = []

        # Validar que el nombre no esté vacío
        if not nombre:
            messagebox.showerror("Error", "El nombre del postre no puede estar vacío.")
            # Devolver el foco a la pestaña de recetas
            self.frame.focus_force()
            return
        
        # Recoger datos de los ingredientes
        filas = ingredientes_frame.grid_slaves()
        filas = sorted(filas, key=lambda x: x.grid_info()["row"])  # Ordenar por fila
        
        # Agrupar los widgets en filas lógicas
        num_filas = max(fila.grid_info()["row"] for fila in filas) + 1
        
        # Filtrar widgets por fila actual
        for i in range(num_filas):
            elemento_combobox = next((w for w in filas if isinstance(w, ttk.Combobox) and "elemento" in w.winfo_name() and w.grid_info()["row"] == i), None)
            cantidad_entry = next((w for w in filas if isinstance(w, tk.Entry) and "cantidad" in w.winfo_name() and w.grid_info()["row"] == i), None)

            if elemento_combobox and cantidad_entry: 
                elemento_valor = elemento_combobox.get()
                cantidad_valor = cantidad_entry.get()
                # Validar valores
                if elemento_valor != "Ingrediente..." and cantidad_valor != "Cantidad": 
                    if ' - ' in elemento_valor: # Si contiene el separador
                        partes = elemento_valor.split(' - ')
                        nombre_busqueda = partes[0].title()
                        marca_busqueda = partes[1].title() if len(partes) > 1 else '' 

                        elemento_data = next((item for item in all_elementos 
                                            if item['nombre'].title() == nombre_busqueda and item['marca'].title() == marca_busqueda), None)
                    else: 
                        nombre_busqueda = elemento_valor.title()
                        elemento_data = next((item for item in all_elementos 
                                            if item['nombre'].title() == nombre_busqueda), None)

                    if elemento_data:
                        # Extraer tipo y nombre del ingrediente
                        ingredientes.append({
                            "elemento_id": elemento_data['id'],
                            "cantidad": int(cantidad_valor),
                            "uni_med": partes[2]
                        })
                    else:
                        messagebox.showerror("Error", f"No se encontró el ingrediente o producto '{elemento_valor}'.")
                        return

        if not ingredientes:
            messagebox.showerror("Error", "Debe agregar al menos un ingrediente válido.")
            return

        # Si es tarta no guarda valores de porciones
        if es_tarta_var:
            grande, mini = (0,0)

        try:
            datos_postre = {
                        "nombre": nombre.lower(),
                        "cantidad_ingredientes": len(ingredientes),
                        "ingredientes": ingredientes,
                        "porc_grande": int(grande),
                        "porc_mini": int(mini),
                        "masa_base": incluye_masa_base_var,
                        "es_tarta": es_tarta_var
                        }
            
            if id_postre:
                # Actualizar el trago en la base de datos
                self.recetas_model.update(int(id_postre), datos_postre)  
                messagebox.showinfo("Éxito", "Postre modificado exitosamente.")
                modal.destroy()  
            else: 
                # Guardar el postre en la base de datos
                self.recetas_model.create(datos_postre)  
                messagebox.showinfo("Éxito", "Postre agregado exitosamente.")
                modal.destroy()  
            # Actualizar en el TreeView
            for row in self.tree.get_children():
                self.tree.delete(row)
            # Llenar la tabla
            self.llenar_tabla()
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el postre: {e}")
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()


    def borrar_postre(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona un ingrediente o producto para eliminar.")
            # Devolver el foco a la pestaña 
            self.frame.focus_force()
            return
        
        # Obtener el ID desde los metadatos del TreeView
        selected_item = selected_item[0]
        # Obtener los valores de las columnas del ítem seleccionado
        values = self.tree.item(selected_item, 'values')
        id_item = values[0]

        nombre_postre = values[1] # sin uso actual

        # Confirmar antes de eliminar
        confirm = messagebox.askyesno("Eliminar Postre", "¿Estás seguro de que deseas eliminar este postre?")
        if confirm:

            try:
                self.recetas_model.delete(int(id_item))
                messagebox.showinfo("Eliminado", "El postre ha sido eliminado correctamente.")
                # Devolver el foco a la pestaña
                self.frame.focus_force()
                # Actualizar en el TreeView
                for row in self.tree.get_children():
                    self.tree.delete(row)
                
                # Llenar la tabla
                self.llenar_tabla()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el postre: {e}")
                self.frame.focus_force()

        
    def guardar_masa_basica(self, masa_frame, actualizar_campos):
        confirm = messagebox.askyesno("Actualizar Masa Básica", "¿Estás seguro de que deseas modificar la Masa Básica?")
        if confirm:
            try:
                # Lista para almacenar los ingredientes con su ID y cantidad
                ingredientes_a_guardar = []

                # Iterar sobre las referencias de widgets
                for widget_pair in self.masa_basica_widgets:
                    combobox = widget_pair['combobox']
                    entry = widget_pair['entry']
                    
                    nombre_seleccionado = combobox.get()
                    cantidad_str = entry.get()

                    # Validar si el ingrediente fue seleccionado y la cantidad es válida
                    if nombre_seleccionado != "Ingrediente..." and cantidad_str and cantidad_str.isdigit() and int(cantidad_str) > 0:
                        ingrediente_id = self.ingredientes_full_name_to_id.get(nombre_seleccionado)
                        if ingrediente_id is not None:
                            ingredientes_a_guardar.append({
                                "id": ingrediente_id,
                                "cantidad": int(cantidad_str) 
                            })

                # Limpiar la tabla de masa básica
                self.masa_basica_model.delete_all()

                # Guardar los nuevos ingredientes con sus cantidades
                for item in ingredientes_a_guardar:
                    self.masa_basica_model.create_all(item)

                messagebox.showinfo("Guardar", "La Masa Básica ha sido actualizada.")
                
                # actualizar_campos
                self.masa_basica = self.masa_basica_model.read_all()
                self.cantidad_combobox_masa.set(len(self.masa_basica))
                actualizar_campos(None, self.cantidad_combobox_masa)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron guardar los cambios en la Masa Básica: {e}")

 

    def actualizar(self):
        self.llenar_tabla()
        masa_basica = self.masa_basica_model.read_all()
        self.cantidad_combobox_masa.set(len(masa_basica))
        self.actualizar_campos_masa_base(None, self.cantidad_combobox_masa)
