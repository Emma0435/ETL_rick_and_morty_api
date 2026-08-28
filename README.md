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

### ✅ Load

El módulo `load.py` es responsable de tomar los DataFrames generados por `transform.py` y cargarlos a una base de datos PostgreSQL, usando **SQLAlchemy** (ORM, sintaxis declarativa 2.0) como capa de conexión y mapeo.

### Esquema de la base de datos

Se definieron 4 clases ORM, cada una mapeada a su tabla correspondiente:

- **`Ubicacion`** (`ubicaciones`): id, name, type, dimension, created.
- **`Episodio`** (`episodios`): id, name, air_date, episodio, created.
- **`Personaje`** (`personajes`): id, name, status, species, type, gender, image, created, origin_id y location_id (foreign keys hacia `ubicaciones.id`, nullable — ver nota sobre valores nulos abajo).
- **`Relacion_Personaje_Episodio`** (`relacion_personaje_episodio`): tabla puente para la relación muchos-a-muchos entre personajes y episodios, con **llave primaria compuesta** (`personaje_id` + `episodio_id`), sin columna `id` autoincremental propia.

El orden de carga respeta las dependencias por foreign key: **Ubicaciones → Episodios → Personajes → Relación**.

### Creación de tablas

`crear_tablas()` usa `Base.metadata.create_all(engine)` para generar el esquema en PostgreSQL. Antes de crear, compara (vía `sqlalchemy.inspect`) las tablas ya existentes en la base contra las definidas en el código, e informa por consola si había tablas faltantes por crear o si el esquema ya estaba completo.

### Carga de datos e idempotencia

Cada tabla tiene su propia función de carga (`cargar_ubicaciones`, `cargar_episodios`, `cargar_personajes`, `cargar_relaciones`). Todas siguen el mismo patrón para evitar insertar registros duplicados si el proceso se corre más de una vez:

1. Consultar los identificadores (o combinación de identificadores, en el caso de la tabla de relación) ya existentes en la base de datos.
2. Filtrar el DataFrame de origen para conservar únicamente las filas cuyo identificador no exista todavía en la base.
3. Insertar solo esas filas nuevas con SQLAlchemy `Session`, y hacer `commit()`.

Se optó por este enfoque (en vez de *upsert* o manejo de excepciones) porque la carga de este proyecto es de una sola vez sobre datos históricos que no requieren actualización — no una carga incremental recurrente.

### Manejo de valores nulos y tipos de dato

Durante la carga surgieron dos incompatibilidades entre pandas/numpy y PostgreSQL que se resolvieron explícitamente:

- **`NaN` vs `NULL`**: los ~300 personajes con origen/ubicación "unknown" en la API llegan como `NaN` de numpy tras la transformación. Como `NaN` no es interpretado por psycopg2 como `NULL` de SQL, se convierten explícitamente a `None` (`None if pd.isna(valor) else valor`) antes de insertarlos.
- **`numpy.int64` no adaptable**: en la tabla de relación, cuyas columnas son puramente numéricas, `iterrows()` devuelve escalares `numpy.int64` (en vez de `int` nativo de Python), que psycopg2 no puede adaptar directamente. Se resuelve forzando la conversión con `int()` antes de insertar.

### Configuración de conexión

La conexión a PostgreSQL se define en `config.py` mediante SQLAlchemy `create_engine`, usando un archivo de configuración local (excluido de control de versiones). Ver `config.example.py` para la plantilla de configuración necesaria.

## Requisitos

Ver `requirements.txt`. Entorno virtual recomendado (`venv`).

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python src/extract.py
```