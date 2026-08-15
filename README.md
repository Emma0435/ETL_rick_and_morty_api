# documentación del proyecto
Activar mi entorno virtual con el comando .\venv\Scripts\Activate.ps1 en la terminal

# ETL Rick and Morty

Proyecto educativo de ETL (Extract, Transform, Load) construido en Python, 
usando la [Rick and Morty API](https://rickandmortyapi.com/) como fuente de datos.

## Objetivo

Practicar un pipeline ETL completo: extracción de datos desde una API REST, 
transformación con pandas/numpy, y carga a una base de datos PostgreSQL.

## Estructura del proyecto
etl-rick-and-morty/
├── src/
│ ├── extract.py # Extracción de datos desde la API
│ ├── json/ # Datos crudos cacheados en JSON
│ ├── transform.py # (pendiente)
│ └── load.py # (pendiente)
├── requirements.txt
├── .gitignore
├── .env
└── README.md

## Progreso

### ✅ Extract

- Función `extraer_datos_paginados(url, json_name)` en `src/extract.py`.
- Maneja la paginación de la API (bloque `info.next` de cada respuesta).
- Incluye una pausa (`time.sleep`) entre peticiones para respetar el límite 
  de peticiones de la API (rate limiting) y evitar errores 429.
- Extrae y cachea localmente en JSON los tres recursos principales:
  - Personajes (`/character`)
  - Ubicaciones (`/location`)
  - Episodios (`/episode`)
- Los conteos obtenidos se validaron manualmente contra Postman.

### ⏳ Transform

Pendiente.

### ⏳ Load

Pendiente.

## Requisitos

Ver `requirements.txt`. Entorno virtual recomendado (`venv`).

## Cómo ejecutar

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python src/extract.py
```