# ETL Rick and Morty

Proyecto educativo de ETL (Extract, Transform, Load) construido en Python,
usando la [Rick and Morty API](https://rickandmortyapi.com/) como fuente de datos.

## Objetivo

Practicar un pipeline ETL completo: extracción de datos desde una API REST,
transformación con pandas/numpy, y carga a una base de datos PostgreSQL.

## Estructura del proyecto

```
etl-rick-and-morty/
├── main.py               # Punto de entrada: orquesta extract → transform → load
├── src/
│   ├── __init__.py
│   ├── extract.py        # Extracción de datos desde la API
│   ├── json/              # Datos crudos cacheados en JSON
│   ├── transform.py       # Transformación y validación de integridad
│   ├── load.py            # Definición de esquema ORM y carga a PostgreSQL
│   ├── config.py           # Conexión a la BD (excluido de git)
│   └── config.example.py   # Plantilla de configuración
├── requirements.txt
├── .gitignore
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
- `validacion_integridad(df_personajes, df_ubicaciones, df_episodios, df_relacion)` — recibe los
  4 DataFrames ya construidos y valida, usando diferencia de sets, que no existan IDs "huérfanos"
  (relaciones que apunten a un registro inexistente). Si encuentra errores, detiene el proceso
  con una excepción detallando el problema exacto; si todo está bien, lo confirma por consola.

### ✅ Load

El módulo `load.py` es responsable de tomar los DataFrames generados por `transform.py` y
cargarlos a una base de datos PostgreSQL, usando **SQLAlchemy** (ORM, sintaxis declarativa 2.0)
como capa de conexión y mapeo.

#### Esquema de la base de datos

Se definieron 4 clases ORM, cada una mapeada a su tabla correspondiente:

- **`Ubicacion`** (`ubicaciones`): id, name, type, dimension, created.
- **`Episodio`** (`episodios`): id, name, air_date, episodio, created.
- **`Personaje`** (`personajes`): id, name, status, species, type, gender, image, created,
  origin_id y location_id (foreign keys hacia `ubicaciones.id`, nullable — ver nota sobre
  valores nulos abajo).
- **`Relacion_Personaje_Episodio`** (`relacion_personaje_episodio`): tabla puente para la
  relación muchos-a-muchos entre personajes y episodios, con **llave primaria compuesta**
  (`personaje_id` + `episodio_id`), sin columna `id` autoincremental propia.

El orden de carga respeta las dependencias por foreign key:
**Ubicaciones → Episodios → Personajes → Relación**.

#### Creación de tablas

`crear_tablas()` usa `Base.metadata.create_all(engine)` para generar el esquema en PostgreSQL.
Antes de crear, compara (vía `sqlalchemy.inspect`) las tablas ya existentes en la base contra
las definidas en el código, e informa por consola si había tablas faltantes por crear o si el
esquema ya estaba completo.

#### Carga de datos e idempotencia

Cada tabla tiene su propia función de carga (`cargar_ubicaciones`, `cargar_episodios`,
`cargar_personajes`, `cargar_relaciones`). Todas siguen el mismo patrón para evitar insertar
registros duplicados si el proceso se corre más de una vez:

1. Consultar los identificadores (o combinación de identificadores, en el caso de la tabla de
   relación) ya existentes en la base de datos.
2. Filtrar el DataFrame de origen para conservar únicamente las filas cuyo identificador no
   exista todavía en la base.
3. Insertar solo esas filas nuevas con SQLAlchemy `Session`, y hacer `commit()`.

Se optó por este enfoque (en vez de *upsert* o manejo de excepciones) porque la carga de este
proyecto es de una sola vez sobre datos históricos que no requieren actualización — no una
carga incremental recurrente.

#### Manejo de valores nulos y tipos de dato

Durante la carga surgieron dos incompatibilidades entre pandas/numpy y PostgreSQL que se
resolvieron explícitamente:

- **`NaN` vs `NULL`**: los ~300 personajes con origen/ubicación "unknown" en la API llegan
  como `NaN` de numpy tras la transformación. Como `NaN` no es interpretado por psycopg2 como
  `NULL` de SQL, se convierten explícitamente a `None`
  (`None if pd.isna(valor) else valor`) antes de insertarlos.
- **`numpy.int64` no adaptable**: en la tabla de relación, cuyas columnas son puramente
  numéricas, `iterrows()` devuelve escalares `numpy.int64` (en vez de `int` nativo de Python),
  que psycopg2 no puede adaptar directamente. Se resuelve forzando la conversión con `int()`
  antes de insertar.

#### Configuración de conexión

La conexión a PostgreSQL se define en `src/config.py` mediante SQLAlchemy `create_engine`,
usando un archivo de configuración local (excluido de control de versiones). Ver
`src/config.example.py` para la plantilla de configuración necesaria.

### ✅ Main (orquestación)

`main.py`, en la raíz del proyecto, es el punto de entrada único que ejecuta el pipeline
completo en orden:

1. **Extract** — descarga y cachea en JSON los 3 recursos de la API (personajes, ubicaciones,
   episodios).
2. **Transform** — construye los 4 DataFrames y corre `validacion_integridad()` sobre ellos
   antes de continuar.
3. **Load** — crea las tablas (si no existen) y carga las 4, en el orden de dependencias.

Al vivir `main.py` en la raíz (fuera de `src/`), los módulos internos de `src/` (`extract`,
`transform`, `load`, `config`) se importan entre sí como paquete, usando imports relativos
(`from . import transform`, `from .config import engine`) y un `src/__init__.py`.

## Requisitos

Ver `requirements.txt`. Entorno virtual recomendado (`venv`).

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Copia `src/config.example.py` a `src/config.py` y coloca tus propias credenciales de
PostgreSQL.

## Ejecución

Correr el pipeline completo desde la raíz del proyecto:

```bash
python main.py
```

Esto ejecuta extracción, transformación (con validación de integridad) y carga a PostgreSQL,
en ese orden, con mensajes de progreso por consola en cada etapa.
