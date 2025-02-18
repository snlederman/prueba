--Número de registros por grupo de cp
SELECT cp AS chest_pain_type, COUNT(id) AS number_of_registered_cases
FROM heart_data
GROUP BY cp