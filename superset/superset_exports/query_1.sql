-- Promedio de 'target' por rango de edad
SELECT
      CASE
            WHEN age BETWEEN 20 AND 29 THEN '20-29'
            WHEN age BETWEEN 30 AND 39 THEN '30-39'
            WHEN age BETWEEN 40 AND 49 THEN '40-49'
            WHEN age BETWEEN 50 AND 59 THEN '50-59'
            WHEN age >= 60 THEN '60+'
            ELSE 'Otros'
      END AS age_range,
      AVG(target) AS avg_target
FROM
      heart_data
GROUP BY
      age_range
ORDER BY
      age_range;