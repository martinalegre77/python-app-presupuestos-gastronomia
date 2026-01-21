# Ventana bebidas/ contenedora de pestanias

import tkinter as tk
from tkinter import ttk
from extras import paths, funciones
from .pestanias_bebidas.presupuesto_bebidas_tab import PresupuestoBebidasTab
from .pestanias_bebidas.bebidas_tab import BebidasTab
from .pestanias_bebidas.tragos_tab import TragosTab
from .pestanias_bebidas.extras_tab import ExtrasTab

class BebidasWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(self.master) # ventana secundaria
        self.window.title("Barra de tragos")
        self.window.iconbitmap(paths.ICONO_DRINK)
        self.window.state('zoomed') # maximizar 
        # self.window.attributes('-zoomed', True)  # Linux/macOS
        
        # Crear y configurar las pestañas
        tabs = ttk.Notebook(self.window) 

        # Instanciar cada pestaña
        self.presupuesto_tab = PresupuestoBebidasTab(tabs, self.master)
        self.tragos_tab = TragosTab(tabs, self.master)
        self.bebidas_tab = BebidasTab(tabs, self.master)
        self.extras_tab = ExtrasTab(tabs, self.master)
        
        # Agregar pestañas al notebook
        tabs.add(self.presupuesto_tab.frame, text="Presupuesto")
        tabs.add(self.tragos_tab.frame, text="Tragos")
        tabs.add(self.bebidas_tab.frame, text="Bebidas")
        tabs.add(self.extras_tab.frame, text="Extras")
        tabs.pack(expand=1, fill="both")
        
        tabs.focus() # hace foco en la ventana actual
        tabs.grab_set() # no permite interacción con la ventana principal

        # Maximizar root al cerrar ésta ventana
        self.window.protocol("WM_DELETE_WINDOW", lambda: funciones.on_close(self.master, self.window))
