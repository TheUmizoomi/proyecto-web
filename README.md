# Sistema Web de Control Académico

Proyecto con Flask y datos temporales en memoria (sin base de datos), interfaz tipo dashboard y CRUD de alumnos, docentes y materias.

## Requisitos

- Python 3
- Entorno virtual `.venv` (incluido en el proyecto)

## Ejecutar

1. Activar entorno virtual (PowerShell):
   - `.\.venv\Scripts\Activate.ps1`
2. Instalar dependencias (si hace falta):
   - `pip install -r requirements.txt`
3. Iniciar servidor:
   - `python app.py`
4. Abrir:
   - [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Datos temporales

Los datos viven en memoria dentro de `app.py`:

- `alumnos_data`
- `docentes_data`
- `materias_data`

Al reiniciar la aplicación, se reinician los registros.
