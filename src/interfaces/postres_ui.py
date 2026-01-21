# Ventana de Postres/ contenedora de pestanias

import tkinter as tk
from tkinter import ttk
from extras import paths, funciones
from interfaces.pestanias_postres.ingredientes_tab import IngredientesTab
from interfaces.pestanias_postres.presupuesto_postres_tab import PresupuestoPostresTab
from interfaces.pestanias_postres.recetas_tab import RecetasTab

class PostresWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(self.master) # ventana secundaria
        self.window.title("Postres")
        self.window.iconbitmap(paths.ICONO_DESSERT)
        self.window.state('zoomed') # maximizar 
        # self.window.attributes('-zoomed', True)  # Linux/macOS
        
        # Crear y configurar las pestañas
        tabs = ttk.Notebook(self.window) 

        # Instanciar cada pestaña
        self.presupuesto_tab = PresupuestoPostresTab(tabs, self.master)
        self.recetas_tab = RecetasTab(tabs, self.master)
        self.ingredientes_tab = IngredientesTab(tabs, self.master)

        # Agregar pestañas al notebook
        tabs.add(self.presupuesto_tab.frame, text="Presupuesto")
        tabs.add(self.recetas_tab.frame, text="Postres")
        tabs.add(self.ingredientes_tab.frame, text="Materia prima/ Insumos")
        tabs.pack(expand=1, fill="both")
        
        tabs.focus() # hace foco en la ventana actual
        tabs.grab_set() # no permite interacción con la ventana principal

        # Maximizar root al cerrar ésta ventana
        self.window.protocol("WM_DELETE_WINDOW", lambda: funciones.on_close(self.master, self.window))
