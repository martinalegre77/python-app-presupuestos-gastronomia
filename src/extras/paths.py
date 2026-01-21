# Configuración general de rutas

import os
from pathlib import Path 
import sys 


def get_base_path():
    """
    Determina la ruta base de la aplicación.
    Si se ejecuta como un ejecutable de PyInstaller, usa sys._MEIPass.
    De lo contrario, usa el directorio del script principal.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPass'):
        return Path(sys._MEIPass)
    else:
        return Path(__file__).resolve().parent.parent
    

def get_user_appdata_local_path(app_name):
    """Retorna la ruta a la carpeta 'AppData\\Local\\<app_name>' del usuario.
    """
    if os.name == 'nt':  # Windows
        local_app_data = os.getenv('LOCALAPPDATA')
        if local_app_data:
            return Path(local_app_data) / app_name
        else:
            return Path.home() / "AppData" / "Local" / app_name
    else:  # Unix-like (Linux, macOS)
        return Path.home() / ".local" / "share" / app_name
    

# Nombre de la aplicación
APP_NAME = "AppDePresupuesto"

# Ruta base para los DATOS DE LA APLICACIÓN (bases de datos)
APP_DATA_BASE_PATH = get_user_appdata_local_path(APP_NAME)

# Ruta de la carpeta de bases de datos DENTRO de la carpeta de datos de la app
DATABASE_DIR = APP_DATA_BASE_PATH / 'databases'

# Asegurarse de que la carpeta 'databases' exista
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# Obtener la ruta base de la aplicación para este módulo
BASE_DIR = get_base_path()

# Ruta de la carpeta de plantillas (templates)
TEMPLATES_DIR = BASE_DIR / "templates"

# Rutas específicas de las plantillas
PRESUPUESTO_BARRA_PATH = TEMPLATES_DIR / "presupuesto_barra.png"
INFORME_BARRA_PATH_1 = TEMPLATES_DIR / "informe_barra_1.png"
INFORME_BARRA_PATH_2 = TEMPLATES_DIR / "informe_barra_2.png"
PRESUPUESTO_POSTRES_PATH = TEMPLATES_DIR / "presupuesto_postres.png"
PRESUPUESTO_POSTRES_PATH_2 = TEMPLATES_DIR / "presupuesto_postres_x.png"
INFORME_POSTRES_PATH_1 = TEMPLATES_DIR / "informe_postres_1.png"
INFORME_POSTRES_PATH_2 = TEMPLATES_DIR / "informe_postres_2.png"

# Ruta de la carpeta de recursos
RECURSOS_DIR = BASE_DIR / "recursos"

# Ruta base para guardar los documentos generados (en "Mis Documentos" del usuario)
def get_user_documents_path():
    """Retorna la ruta a la carpeta 'Mis Documentos' del usuario."""
    return Path.home() / "Documents"

# Nombre de la carpeta raíz dentro de Documentos
APP_DOCS_DIR_NAME = "Presupuestos e Informes" 
# Ruta base: "Mis Documentos/Presupuestos e Informes"
APP_DOCS_BARRA_PATH = get_user_documents_path() / APP_DOCS_DIR_NAME
# Rutas para las subcarpetas específicas
APP_INFORMES_PATH = APP_DOCS_BARRA_PATH / "Informes"
APP_PRESUPUESTOS_PATH = APP_DOCS_BARRA_PATH / "Presupuestos"

# Icono
ICONO = BASE_DIR / "imagenes" / "icono.ico"
ICONO_DRINK = BASE_DIR / "imagenes" / "icono_drink.ico"
ICONO_DESSERT = BASE_DIR / "imagenes" / "icono_dessert.ico" 

# Imagenes
LOGO_PATH = BASE_DIR / "imagenes" / "logo.png"
FONDO_APP = BASE_DIR / "imagenes" / "barra.jpg"

# Crear los directorios cuando se inicializa la aplicación o antes de usarlos
APP_INFORMES_PATH.mkdir(parents=True, exist_ok=True)
APP_PRESUPUESTOS_PATH.mkdir(parents=True, exist_ok=True)
RECURSOS_DIR.mkdir(parents=True, exist_ok=True) # Crea el directorio de recursos si no existe
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True) # Asegura de que 'templates' exista
(BASE_DIR / "imagenes").mkdir(parents=True, exist_ok=True) # Asegura de que 'imagenes' exista
