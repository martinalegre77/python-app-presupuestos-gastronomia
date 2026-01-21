# 📐 Arquitectura de la Aplicación

## 🧩 Visión General

La aplicación de presupuestos fue diseñada como una **aplicación de escritorio modular**, desarrollada en Python, con una arquitectura orientada a la **separación de responsabilidades** y facilidad de mantenimiento.

El sistema no depende de servicios externos ni de un backend remoto, lo que permite su uso en entornos locales, ideal para pequeños negocios y emprendimientos gastronómicos.

---

## 🏗️ Arquitectura General

La arquitectura se organiza en capas claramente diferenciadas:

Interfaz Gráfica (Tkinter)
│
▼
Lógica de Negocio
│
▼
Persistencia de Datos (TinyDB)


Cada capa cumple una función específica y se comunica de manera controlada con las demás.

---

## 📂 Estructura de Carpetas

### `src/`
Contiene el código fuente principal de la aplicación.

#### `interfaces/`
- Implementa la **interfaz gráfica de usuario** mediante Tkinter
- Maneja ventanas, formularios, pestañas y eventos
- No contiene lógica de negocio compleja

Ejemplos:
- `main_window.py`
- `bebidas_ui.py`
- `postres_ui.py`

---

#### `logica/`
- Contiene la **lógica de negocio**
- Cálculos de costos, cantidades y precios
- Generación de presupuestos e informes

Ejemplos:
- `calculos_bebidas.py`
- `calculos_postres.py`
- `informes_bebidas.py`
- `informes_postres.py`

---

#### `modelos/`
- Maneja la **persistencia de datos**
- Define estructuras y acceso a TinyDB
- Aísla la base de datos del resto del sistema

Ejemplos:
- `models.py`
- `db_manager.py`

---

#### `extras/`
- Utilidades y configuraciones auxiliares
- Manejo de rutas, constantes y helpers generales

---

## 🗄️ Persistencia de Datos

La aplicación utiliza **TinyDB** como base de datos NoSQL, almacenada en archivos JSON locales.

### Motivos de elección:
- No requiere servidor
- Fácil portabilidad
- Ideal para aplicaciones de escritorio
- Bajo overhead

El acceso a datos se centraliza en el módulo `db_manager.py`, evitando accesos directos desde la interfaz gráfica.

---

## 📄 Generación de Documentos

Los presupuestos e informes se generan en **formato PDF**, integrando:
- Detalle de ingredientes
- Insumos utilizados
- Costos parciales y totales
- Estimación de ganancia

Esta funcionalidad se encuentra desacoplada de la interfaz, facilitando futuras mejoras o cambios de formato.

---

## 🔁 Flujo de Funcionamiento

1. El usuario interactúa con la interfaz gráfica
2. La interfaz solicita operaciones a la capa de lógica
3. La lógica consulta o persiste datos mediante el módulo de modelos
4. Se generan resultados (presupuestos / informes)
5. El usuario obtiene el PDF final

---

## 🔒 Consideraciones de Seguridad

- La aplicación no expone servicios externos
- Los datos se almacenan localmente
- No se incluyen credenciales ni información sensible en el repositorio público
- El diseño permite futuras extensiones (encriptación, backups)

---

## 🚀 Escalabilidad y Extensiones

La arquitectura permite:
- Agregar nuevos tipos de productos
- Incorporar control de stock
- Integrar exportación contable
- Migrar a una base de datos relacional si el contexto lo requiere

---

## ✅ Conclusión

La aplicación fue diseñada con un enfoque pragmático, priorizando:
- Claridad estructural
- Mantenibilidad
- Separación de responsabilidades
- Adaptabilidad a entornos reales de uso comercial
