# Especificación de Requisitos de Software (SRS)
## Proyecto: Gestor de Menú y Compra Automatizada "Zero-Waste"
**Versión:** 1.0  
**Fecha:** 26 de mayo de 2026

---

## 1. Introducción
El objetivo de este documento es definir los requisitos técnicos y funcionales para una aplicación web diseñada para la planificación de menús multi-usuario y la automatización de listas de la compra. El sistema busca optimizar la logística del hogar, eliminando el desperdicio de alimentos mediante la gestión por paquetes completos.

## 2. Descripción General del Sistema
* **Modelo de Operación:** El Menú es la fuente de verdad. El sistema consolida las necesidades de compra de múltiples usuarios en una lista única y agregada.
* **Restricción de Inventario:** La unidad mínima de gestión es el **Paquete/Envase**. No se realizan cálculos de gramos ni gestión de inventario de sobras; el sistema garantiza que los insumos requeridos estén disponibles.

## 3. Requisitos Funcionales (RF)

### 3.1 Módulo de Catálogo
* **RF0.1:** Gestión de **Categorías de Producto**: El usuario podrá crear, editar y eliminar categorías (ej. Frutería, Carnicería).
* **RF0.2:** Gestión de **Ingredientes**: Registro de ingredientes asociados obligatoriamente a una `Categoría_Producto` y marcados como `es_fresco` (bool).

### 3.2 Módulo de Recetas
* **RF1.1:** Creación de recetas con nombre, instrucciones detalladas de preparación y lista de ingredientes vinculados.
* **RF1.2:** Asignación de cantidades enteras (`cantidad_paquetes`) por ingrediente.

### 3.3 Módulo de Planificación (Menú)
* **RF2.1:** Gestión de **Usuarios**: Registro de múltiples usuarios con un color identificativo único para representación visual.
* **RF2.2:** **Planificador Colaborativo**: Visualización de calendario (semanal/mensual) que muestra las comidas de todos los usuarios, diferenciadas por color.
* **RF2.3:** **Generación de Menú**: Soporte para planificación manual o aleatoria (con edición posterior).

### 3.4 Módulo de Lista de la Compra
* **RF3.1:** **Consolidación Inteligente**: Suma total de paquetes necesarios para todos los usuarios.
* **RF3.2:** **Agrupación**: La lista de la compra debe estar categorizada según `Categoría_Producto`.
* **RF3.3:** **Agenda de Compras**: 
    * **Lista de Carga:** Ingredientes no frescos (compra semanal).
    * **Lista de Frescos:** Programados según la fecha de consumo ($D_r$ o $D_r-1$).

## 4. Lógica de Negocio

### 4.1 Cálculo de Fecha de Compra ($F_c$)
Para cada ingrediente $i$ en un día de receta $D_r$:
$$F_c(i) = 
\begin{cases} 
D_r - \{0, 1\} & \text{si } i.es\_fresco = \text{True} \\
\text{Viernes previo} & \text{si } i.es\_fresco = \text{False}
\end{cases}$$

### 4.2 Algoritmo de Consolidación
Para todos los usuarios $U$ en el rango de días $n$:
$$Total\_Paquetes(i) = \sum_{d=1}^{n} \sum_{u \in U} \text{cantidad\_paquetes}(i, r_{u,d})$$

## 5. Modelo de Datos (Esquema Relacional)

* **Categoría_Producto:** `id`, `nombre`.
* **Ingrediente:** `id`, `nombre`, `es_fresco`, `id_categoria` (FK).
* **Usuario:** `id`, `nombre`, `color_hex`.
* **Receta:** `id`, `nombre`, `instrucciones` (text).
* **Receta_Ingrediente:** `id_receta`, `id_ingrediente`, `cantidad_paquetes` (int).
* **Calendario_Menu:** `id`, `fecha`, `id_usuario` (FK), `id_receta` (FK), `tipo_comida` (desayuno, comida, cena).

## 6. Stack Tecnológico
* **Frontend:** React.js (Drag & Drop, interfaz reactiva).
* **Backend:** Python (FastAPI, tipado robusto).
* **Base de Datos:** PostgreSQL (Integridad relacional).
* **Infraestructura:** Oracle Cloud (Docker).

## 7. Criterios de Aceptación
1. Visualización multi-usuario clara en calendario.
2. Lista de compra categorizada por pasillos.
3. Actualización automática de compras ante cambios en el menú.