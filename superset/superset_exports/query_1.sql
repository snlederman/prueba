-- Promedio de 'target' por rango de edad

SELECT 
    CASE 
        WHEN age BETWEEN 20 AND 30 THEN '20-30'
        WHEN age BETWEEN 31 AND 40 THEN '31-40'
        WHEN age BETWEEN 41 AND 50 THEN '41-50'
        WHEN age BETWEEN 51 AND 60 THEN '51-60'
        WHEN age BETWEEN 61 AND 70 THEN '61-70'
        ELSE '71+'
    END AS rango_edad,
    ROUND(AVG(target)::numeric, 2) AS promedio_target,
    COUNT(*) AS cantidad_pacientes
FROM heart_data
GROUP BY rango_edad
ORDER BY rango_edad;