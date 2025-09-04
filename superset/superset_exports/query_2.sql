-- Numero de registros por grupo de -cp
SELECT
      cp,
      COUNT(*) AS count_of_records
FROM
      heart_data
GROUP BY
      cp
ORDER BY
      cp;