/**
  * RETO:   Encontrar el promedio de alumnos por tutor
  */

SELECT AVG(alumnos_por_tutor) promedio_alumnos_por_tutor
FROM (
	SELECT	CONCAT(t.nombre, ' ', t.apellido) AS tutor,
			COUNT(*) AS alumnos_por_tutor
	FROM	platzi.alumnos AS a
		INNER JOIN platzi.alumnos AS t ON a.tutor_id = t.id
	GROUP BY tutor
) alumnos_tutor;


/**
  * Operaciones con la misma tabla
  */
-- Alumnos por carrera --
SELECT	carrera_id, count(*) AS cuenta
FROM platzi.alumnos
GROUP BY carrera_id
ORDER BY cuenta DESC;

-- Borrar carreras con id entre 30 y 40 --
DELETE FROM platzi.carreras
WHERE id BETWEEN 30 AND 40;

-- Exlusive left join --
SELECT 	a.nombre,
		a.apellido,
		a.carrera_id,
		c.id,
		c.carrera
FROM	platzi.alumnos AS a
	LEFT JOIN platzi.carreras AS c
	ON a.carrera_id = c.id
WHERE c.id IS NULL;