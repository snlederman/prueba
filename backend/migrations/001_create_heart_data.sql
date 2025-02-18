-- Archivo: 001_create_heart_data.sql

-- Creación de la tabla de staging: heart_data_staging
-- Esta tabla se utiliza para cargar los datos tal como vienen del CSV, sin restricciones de integridad
-- (se permiten NULLs y duplicados). Posteriormente se aplicarán pruebas de calidad y se migrarán solo los
-- registros válidos a la tabla de producción.
CREATE TABLE IF NOT EXISTS heart_data_staging (
    id INTEGER,
    age INTEGER,
    sex INTEGER,
    cp INTEGER,
    trestbps INTEGER,
    chol INTEGER,
    fbs INTEGER,
    restecg INTEGER,
    thalach INTEGER,
    exang INTEGER,
    oldpeak DECIMAL,
    slope INTEGER,
    ca INTEGER,
    thal INTEGER,
    target INTEGER
);

-- Creación de la tabla de producción: heart_data
CREATE TABLE IF NOT EXISTS heart_data (
    id INTEGER PRIMARY KEY UNIQUE,
    age INTEGER NOT NULL,
    sex INTEGER NOT NULL,
    cp INTEGER NOT NULL,
    trestbps INTEGER NOT NULL,
    chol INTEGER NOT NULL,
    fbs INTEGER NOT NULL,
    restecg INTEGER NOT NULL,
    thalach INTEGER NOT NULL,
    exang INTEGER NOT NULL,
    oldpeak DECIMAL NOT NULL,
    slope INTEGER NOT NULL,
    ca INTEGER NOT NULL,
    thal INTEGER NOT NULL,
    target INTEGER NOT NULL
    -- #TODO: Define la columna `id` como PRIMARY KEY.
    -- #TODO: Agrega el resto de las columnas, estableciendo NOT NULL en cada una según el Data Dictionary del CSV.
    -- #TODO: Agrega una restricción UNIQUE para evitar duplicados.
);