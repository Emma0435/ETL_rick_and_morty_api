-- Bloque 3 — Agregaciones
-- COUNT, SUM, AVG, MIN, MAX
-- GROUP BY
-- HAVING vs WHERE
-- Ejemplo natural: "¿cuántos personajes hay por especie?" o "¿cuántos episodios por temporada?"


-- TEORIA
-- Funciones de agregación básicas
SELECT COUNT(*) as cantidad_perosnajes FROM personajes; -- cuantas filas hay
SELECT COUNT (origin_id) as cantidad_origenes FROM personajes; -- cuántas filas con origin_id NO nulo (ojo, COUNT ignora NULLs excepto con *)
SELECT AVG(id) as promedio_ids FROM personajes; -- promedio (ejemplo trivial, normalmente sobre columnas numéricas con sentido)
SELECT MIN(created) as episodio_mas_antiguo, MAX(created) as episodio_mas_nuevo FROM personajes; -- registro más antiguo y más reciente

-- GROUP BY — agrupar antes de agregar
-- Sin GROUP BY, las funciones de agregación colapsan toda la tabla en una fila. Con GROUP BY, colapsan cada grupo en una fila
-- Regla de oro: toda columna en el SELECT que no esté dentro de una función de agregación debe aparecer en el GROUP BY. Si lo olvidas,
-- PostgreSQL te tira error (a diferencia de MySQL, que a veces lo deja pasar silenciosamente con resultados ambiguos).
SELECT species, COUNT(*) AS cantidad
FROM personajes
GROUP BY species;


-- HAVING vs WHERE — la diferencia que más confunde
-- WHERE filtra filas individuales, antes de agrupar.
-- HAVING filtra grupos ya formados, después de agrupar/agregar.

-- INCORRECTO — WHERE no puede usar COUNT()
-- SELECT especie, COUNT(*) 
-- FROM personajes
-- WHERE COUNT(*) > 10   -- ❌ error
-- GROUP BY especie;

-- CORRECTO
SELECT species, COUNT(*) AS cantidad
FROM personajes
GROUP BY species
HAVING COUNT(*) >10;

-- Contamos las especies donde el status es estar vivo y hay más de 10
SELECT species, COUNT (*) AS cantidad
FROM personajes
WHERE status = 'Alive'
GROUP BY species
HAVING COUNT (*) > 10;


-- EJERCICIO
-- 1. ¿Cuántos personajes hay por cada status (Alive, Dead, unknown)?
SELECT status AS estado_personajes, COUNT (*) AS cantidad
FROM personajes
GROUP BY status;

-- 2 . ¿Cuántos episodios hay por cada valor de la columna episodio truncado al primer código de temporada?
-- Para esto tuve que truncar, que es tomar los primeros 3 caracteres (la temporada) y después contar su cantidad
-- y finalmente agruparlas por temporadas
SELECT LEFT(episodio, 3) AS temporada, 
COUNT(*) AS cantidad_capitulos
FROM episodios
GROUP BY LEFT(episodio, 3);

-- 3. ¿Qué especies tienen más de 50 personajes registrados?
SELECT species, COUNT(*) as cantidad
FROM personajes
GROUP BY species
HAVING COUNT(*) >50;