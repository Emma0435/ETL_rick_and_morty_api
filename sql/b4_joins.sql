-- Bloque 4 — JOINs
-- INNER JOIN
-- LEFT JOIN / RIGHT JOIN
-- FULL OUTER JOIN
-- Self-join si aplica algún caso
-- Aquí es donde tu tabla puente relacion_personaje_episodio y las FKs hacia ubicaciones cobran sentido real



-- INNER JOIN 
-- Busca lo que hay en común entre 2 tablas distintas, buscando el id en común y retornando los nombres en este caso
-- (vemos cuantos personajes y ubicaciones estan relacionados)
SELECT personajes.name as nombre_personaje, ubicaciones.name as ubicacion_actual
FROM personajes
INNER JOIN ubicaciones ON personajes.location_id = ubicaciones.id;

-- Comparación: vemos que el inner join tiene menos cantidad de registros porque omite los nulos
-- (personajes con ubicación desconocida)
SELECT COUNT(*) AS cantidad_personajes
FROM personajes;
SELECT COUNT(*) AS cantidad
FROM personajes
INNER JOIN ubicaciones ON personajes.location_id = ubicaciones.id;



-- LEFT JOIN
-- Selecciona toda la tabla de la izquierda (personajes) y muestra su relación con la de la derecha
-- En este caso no omite los nulos porque estamos priorizando la tabla izquierda, no lo que hay en común entre ambas
SELECT personajes.name AS nombre_personaje, ubicaciones.name AS ubicacion_actual
FROM personajes
LEFT JOIN ubicaciones ON personajes.location_id = ubicaciones.id;

-- Aqui vemos a todos los personajes que no tienen ubicaciones
SELECT personajes.name AS nombre_personaje, ubicaciones.name AS ubicacion_actual
FROM personajes
LEFT JOIN ubicaciones ON personajes.location_id = ubicaciones.id
WHERE personajes.location_id IS NULL;

-- Con esta consulta confirmamos que es la misma cantidad de registros que la cantidad de personajes
-- Es decir, no se omitieron los nulos
SELECT COUNT(*) AS cantidad
FROM personajes
LEFT JOIN ubicaciones ON personajes.location_id = ubicaciones.id;


-- RIGHT JOIN
-- Es lo mismo que el left join, pero esta vez priorizando la tabla de la derecha
-- El resultado es exactamente el mismo que left join, la unica diferencia es el acomodo de la sintaxis
SELECT personajes.name AS personaje_nombre, ubicaciones.name AS ubicacion_actual
FROM ubicaciones
RIGHT JOIN personajes ON personajes.location_id = ubicaciones.id;


-- FULL OUTER JOIN
-- Es la combinación de left y right join, se consultan ambas tablas tengan coincidencia o no
SELECT personajes.name as personaje, ubicaciones.name as ubicacion_actual
FROM personajes 
FULL OUTER JOIN ubicaciones ON personajes.location_id = ubicaciones.id;

-- Aqui vemos las ubicaciones que no tienen personajes
SELECT ubicaciones.name as ubicacion, personajes.name as personaje
FROM ubicaciones
LEFT JOIN personajes ON personajes.location_id = ubicaciones.id
WHERE personajes.location_id IS NULL;