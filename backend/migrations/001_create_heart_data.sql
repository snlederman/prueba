001_create_customer_feedback.sql:
-- Archivo: 001_create_heart_data.sql

-- Creación de la tabla de staging: heart_data_staging
CREATE TABLE IF NOT EXISTS heart_data_staging (
    -- #TODO: Agrega las columnas según el Data Dictionary del CSV
);
-- Nota: La restricción UNIQUE en la tabla de staging es opcional, ya que se puede aplicar la idempotencia al insertar en la tabla de producción.

-- Creación de la tabla de producción: heart_data
CREATE TABLE IF NOT EXISTS heart_data (
    -- #TODO: Establece la columna `id` como PRIMARY KEY
    -- #TODO: Agrega las demás columnas según el Data Dictionary del CSV
    -- #TODO: Agrega una restricción UNIQUE que evite duplicados
);