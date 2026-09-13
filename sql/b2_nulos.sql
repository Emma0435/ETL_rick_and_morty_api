-- Bloque 2 — Trabajo con valores nulos y tipos
-- IS NULL / IS NOT NULL (muy relevante: tienes origin_id/location_id nulos)
-- COALESCE, NULLIF
-- Casting de tipos (::, CAST)
-- Funciones de fecha (útil con air_date, created)


-- Teoría

-- 1. IS NULL / IS NOT NULL
-- NULL no es un valor, es la ausencia de valor — por eso = NULL nunca funciona (ni siquiera NULL = NULL es verdadero). Se compara con un operador especial:
SELECT name 
FROM personajes
WHERE origin_id IS NULL;

SELECT NAME 
FROM personajes
WHERE location_id IS NOT NULL;


-- 2. COALESCE — primer valor no nulo
-- busca NULLs y los reemplaza por el primer valor no nulo que le des.
SELECT name,
COALESCE(origin_id::text, 'Sin origen') AS origen
FROM personajes;


-- 3. NULLIF — lo opuesto en cierto sentido
-- busca una coincidencia exacta entre dos valores; si la encuentra, la convierte en NULL.
SELECT NULLIF(species, 'unknown') as especies
FROM personajes;


-- 4. Casting de tipos: :: y CAST
-- Dos sintaxis equivalentes en PostgreSQL
-- :: es más corto pero es específico de PostgreSQL; CAST(...) es estándar SQL y funciona en otros motores.
-- cambia el tipo de dato solo para esa consulta (el resultado que ves), no modifica la columna real en la tabla
SELECT origin_id::text FROM personajes;
SELECT CAST(origin_id AS text) FROM personajes;


-- 5 . Funciones de fecha
-- Extraemos unicamente el año de la fecha
SELECT episodio,
EXTRACT (YEAR FROM air_date) as anio_lanzamiento
FROM episodios;

-- extraemos solo la fecha (por el tipo de dato también contiene la hora)
SELECT air_date::date AS solo_fecha
FROM episodios;

-- calculamos una edad, con el parametro now, y la fecha de creación del personaje
SELECT AGE(now(), created) AS antiguedad
FROM personajes;




-- EJERCICIO
-- Sobre personajes, escribe una consulta que:
-- 1. Muestre nombre y una columna origen que diga el origin_id convertido a texto, o 'Desconocido' si es nulo
SELECT name, 
COALESCE (origin_id::text, 'Origen desconocido') as origen
FROM personajes;

-- 2. y además muestre el año en que fue creado el registro (created)
SELECT name as nombre_personaje,
COALESCE (origin_id::text, 'Origen desconocido') as origen,
EXTRACT (YEAR FROM created) as creado_en
FROM personajes;

-- 3. Sobre personajes, muestra nombre de los personajes que no tienen ni origin_id ni location_id (ambos nulos a la vez).
SELECT name,
COALESCE (origin_id::text, 'Sin origen') as origen,
COALESCE (location_id::text, 'Sin ubicacion') as ubicacion
FROM personajes
WHERE origin_id IS NULL AND location_id IS NULL;

-- 4. Sobre personajes, muestra nombre y una columna ubicacion_final que devuelva location_id si existe, y si no, origin_id, y si tampoco existe, el texto 'Sin datos'.
SELECT name,
COALESCE (location_id::text, origin_id::text, 'Sin datos') as ubicacion_final
FROM personajes;

-- 5. Sobre episodios, muestra name de los episodios donde el año de air_date sea igual a 2017
SELECT episodio, name,
EXTRACT (YEAR FROM air_date) as anio
FROM episodios
WHERE EXTRACT (YEAR FROM air_date) = 2017;