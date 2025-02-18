-- Promedio de 'target' por rango de edad

SELECT
  CASE
    WHEN age BETWEEN 0 AND 40 THEN '0-40'
    WHEN age BETWEEN 40 AND 50 THEN '40-50'
    WHEN age BETWEEN 50 AND 60 THEN '50-60'
    ELSE '60+'
  END AS age_range,
  AVG(target) AS average_target
FROM heart_data
GROUP BY age_range
ORDER BY age_range;