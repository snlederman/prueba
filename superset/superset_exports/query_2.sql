-- Numero de registros por grupo de -cp
SELECT
  cp, COUNT(*) AS logs_number
FROM heart_data
GROUP BY cp
ORDER BY cp;