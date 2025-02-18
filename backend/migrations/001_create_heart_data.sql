-- Archivo: 001_create_heart_data.sql

-- Creación de la tabla de staging: heart_data_staging
-- Esta tabla se utiliza para cargar los datos tal como vienen del CSV, sin restricciones de integridad
-- (se permiten NULLs y duplicados). Posteriormente se aplicarán pruebas de calidad y se migrarán solo los
-- registros válidos a la tabla de producción.
CREATE TABLE IF NOT EXISTS heart_data_staging (
    -- #TODO: Agrega las columnas según el Data Dictionary del CSV
);

-- Creación de la tabla de producción: heart_data
CREATE TABLE IF NOT EXISTS heart_data (
    -- #TODO: Define la columna `id` como PRIMARY KEY.
    -- #TODO: Agrega el resto de las columnas, estableciendo NOT NULL en cada una según el Data Dictionary del CSV.
    -- #TODO: Agrega una restricción UNIQUE para evitar duplicados.
);