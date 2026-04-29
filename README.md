# Sistema de Control Académico

Sistema web desarrollado con Flask y MongoDB para la gestión de alumnos, docentes, materias y calificaciones.

## Descripción

El sistema permite administrar información académica mediante una interfaz web organizada por módulos. Incluye operaciones CRUD completas, validaciones de datos y visualización de información en tiempo real.

## Tecnologías utilizadas

- Python
- Flask
- MongoDB
- PyMongo
- HTML, CSS, JavaScript
- Jinja2

## Estructura del proyecto
/app.py
/models
/routes
/templates
/static


## Funcionalidades

### Módulo de Alumnos
- Registro
- Edición
- Eliminación
- Consulta

### Módulo de Docentes
- Registro
- Edición
- Eliminación

### Módulo de Materias
- Registro
- Edición
- Eliminación
- Asignación de docente

### Módulo de Calificaciones
- Registro de calificaciones
- Edición
- Consulta por alumno
- Asignación automática de periodo

## Requisitos

- Python 3.10 o superior
- MongoDB Community Server
- Navegador web actualizado

## Instalación

Clonar el repositorio:
git clone []
cd nombre-del-proyecto

Crear entorno virtual:
python -m venv venv

Activar entorno virtual:
Windows:
venv\Scripts\activate

Linux/macOS:
source venv/bin/activate

Instalar dependencias:
pip install flask pymongo

## Configuración de la base de datos

Asegurarse de que MongoDB esté en ejecución.

La base de datos utilizada es:


control_academico


Las colecciones se generan automáticamente:
- alumnos
- docentes
- materias
- calificaciones

## Ejecución


python app.py


Acceder en el navegador:
http://127.0.0.1:5000

## Autor

Proyecto desarrollado como parte de la materia de programación web.

- Carlos Rafael Martínez Hernández
- Montserrat Jacqueline Betanzos Hernández
