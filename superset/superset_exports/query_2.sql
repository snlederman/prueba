<<<<<<< HEAD
-- Numero de registros por grupo de -cp

SELECT
    cp,
    COUNT(*) AS numero_registros
FROM
    heart_data
GROUP BY
    cp
ORDER BY
    numero_registros DESC;
=======
-- Numero de registros por grupo de -cp
>>>>>>> c74c09c17a7461041a093096b42c637a29b01ed6
