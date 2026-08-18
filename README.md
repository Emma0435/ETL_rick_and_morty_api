Activar mi entorno virtual con el comando .\venv\Scripts\Activate.ps1 en la terminal

# ETL Rick and Morty

Proyecto educativo de ETL (Extract, Transform, Load) construido en Python, 
usando la [Rick and Morty API](https://rickandmortyapi.com/) como fuente de datos.

## Objetivo

Practicar un pipeline ETL completo: extracción de datos desde una API REST, 
transformación con pandas/numpy, y carga a una base de datos PostgreSQL.

## Estructura del proyecto
```
etl-rick-and-morty/
├── src/
│   ├── extract.py      # Extracción de datos desde la API
│   ├── json/            # Datos crudos cacheados en JSON
│   ├── transform.py     # Transformación y validación de integridad
│   └── load.py          # (pendiente)
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

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

### ✅ Transform

- Funciones en `src/transform.py`, cada una devuelve un DataFrame listo para cargar:
  - `crear_tabla_personajes()` — aplana `origin`/`location` (dict → `origin_id`/`location_id`), 
    descarta la relación con episodios (se maneja aparte, ver tabla puente).
  - `crear_tabla_ubicaciones()` — descarta `residents` y `url` (personajes es la fuente de verdad 
    para las relaciones).
  - `crear_tabla_episodios()` — descarta `characters` y `url` por el mismo motivo.
  - `crear_relacion_personaje_episodio()` — tabla puente (`character_id`, `episode_id`) construida 
    con `.explode()` sobre la lista de episodios de cada personaje, para modelar la relación 
    muchos-a-muchos.
- `validacion_integridad()` — valida, usando diferencia de sets, que no existan IDs "huérfanos" 
  (relaciones que apunten a un registro inexistente) entre las 4 tablas. Si encuentra errores, 
  detiene el proceso con una excepción detallando el problema exacto.

### ⏳ Load

Pendiente. `load.py` importará las funciones de `transform.py` directamente (sin archivos 
intermedios en disco) y cargará los DataFrames resultantes a PostgreSQL.

## Requisitos

Ver `requirements.txt`. Entorno virtual recomendado (`venv`).

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python src/extract.py
```