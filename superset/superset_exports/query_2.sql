-- Numero de registros por grupo de -cp

SELECT 
    cp,
    CASE 
        WHEN cp = 0 THEN 'Típica'
        WHEN cp = 1 THEN 'Atípica'
        WHEN cp = 2 THEN 'No anginal'
        WHEN cp = 3 THEN 'Asintomática'
        ELSE 'Desconocido'
    END AS tipo_dolor_pecho,
    COUNT(*) AS cantidad_pacientes,
    ROUND(AVG(target)::numeric, 2) AS tasa_enfermedad
FROM heart_data
GROUP BY cp
ORDER BY cp;