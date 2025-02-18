--Obtener el promedio de target por rango de edad
SELECT CASE WHEN age <= 20 THEN '<20'
            WHEN   age>20 AND age <=40 THEN '21 - 40'
            WHEN   age>40 AND age <= 60 THEN '41 - 60'
            WHEN   age> 60 AND age <= 80 THEN '61 - 80'
            WHEN   age > 80 THEN '>80' END AS age_range, AVG(target) AS average_disease_probability
FROM heart_data
GROUP BY age_range