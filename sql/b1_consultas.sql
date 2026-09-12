-- TEORIA
-- Seleccionar todo de personajes
SELECT * FROM personajes;

-- Seleccionar columnas especificas
SELECT id, name, gender FROM personajes;

-- Seleccionar y renombrar columnas
SELECT name as personaje, image as imagen_url FROM personajes;

-- Selección de valores existentes en una columna (DISTINCT)
SELECT DISTINCT species FROM personajes;

-- Seleccionamos columnas y ordenamos por el genero (ORDER BY)
SELECT name, gender FROM personajes ORDER BY gender DESC; --(Descendente)
SELECT name, gender FROM personajes ORDER BY gender ASC; -- (Ascendente)

-- Seleccionamos los primeros 10 resultados (LIMIT)
SELECT name as nombre_personaje FROM personajes LIMIT 10;



-- EJERCICIOS 
-- 1. Muestre el nombre y la fecha de emisión de los episodios
SELECT name as nombre_episodio, air_date as fecha_de_emision 
FROM episodios;

-- 2. sin repetir nombres
SELECT DISTINCT name as nombre_episodio, air_date as fecha_de_emision 
FROM episodios; 

-- 3. ordenados por fecha de emisión de más reciente a más antiguo
SELECT DISTINCT name as nombre_episodio, air_date as fecha_de_emision
FROM episodios
ORDER BY air_date DESC;

-- 4. mostrando solo los primeros 5
SELECT DISTINCT name as nombre_episodio, air_date as fecha_de_emision
FROM episodios
ORDER BY air_date DESC
LIMIT 5;



-- TEORIA
-- Filtramos solo los que estan vivos (WHERE)
-- Operadores de comparación: =, <> (o !=), <, >, <=, >=
SELECT name as nombre, status as estado 
FROM personajes 
WHERE status = 'Alive';
-- Misma consulta pero con combinacion de condiciones
SELECT name as nombre, status as estado, species as especie
FROM personajes 
WHERE status = 'Alive' and species = 'Human';

-- Definicion de un rango (BETWEEN _ AND _)
SELECT name as nombre_personaje, origin_id as id_origen
FROM personajes
WHERE origin_id BETWEEN 1 AND 20;

-- Es un igual a "species = 'Alien'" pero con 2 o más valores
SELECT name as nombre_personaje, species as especie
FROM personajes
WHERE species IN ('Human', 'Alien');

-- Seleccionamos donde un personaje empieza con (en este caso rick)
SELECT name 
FROM personajes 
WHERE name LIKE 'Rick%';

-- Seleccionamos todos los valores nulos (usar = NULL, no funciona)
SELECT name, origin_id FROM personajes 
WHERE origin_id IS NULL;



-- EJERCICIOS
-- Sobre personajes, escribe una consulta que muestre nombre y especie de los personajes que:
-- 1. Estén vivos
SELECT name as nombre, status as estado
FROM personajes 
WHERE status = 'Alive';

-- 2. sean de especie 'Human' o 'Alien'
SELECT name as nombre, species as especie
FROM personajes 
WHERE species IN ('Human', 'Alien');

-- 3. cuyo nombre empiece con la letra M
SELECT name as nombre
FROM personajes 
WHERE name LIKE 'M%';

-- 4. todas las anteriores
SELECT name as nombre, species as especie, status as estado
FROM personajes
WHERE name LIKE 'M%' AND
species IN ('Human', 'Alien') AND
status = 'Alive';