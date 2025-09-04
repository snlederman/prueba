-- Archivo: 001_create_heart_data.sql

-- Creación de la tabla de staging: heart_data_staging
-- Esta tabla se utiliza para cargar los datos tal como vienen del CSV, sin restricciones de integridad
-- (se permiten NULLs y duplicados). Posteriormente se aplicarán pruebas de calidad y se migrarán solo los
-- registros válidos a la tabla de producción.
CREATE TABLE IF NOT EXISTS heart_data_staging (
    id INT,
    age INT,
    sex INT,
    cp INT,
    trestbps INT,
    chol INT,
    fbs INT,
    restecg INT,
    thalach INT,
    exang INT,
    oldpeak FLOAT,
    slope INT,
    ca INT,
    thal INT,
    target INT
);

-- Creación de la tabla de producción: heart_data
CREATE TABLE IF NOT EXISTS heart_data (
    -- #TODO: Define la columna `id` como PRIMARY KEY.
    -- #TODO: Agrega el resto de las columnas, estableciendo NOT NULL en cada una según el Data Dictionary del CSV.
    -- #TODO: Agrega una restricción UNIQUE para evitar duplicados.
    id INT PRIMARY KEY UNIQUE,
    age INT NOT NULL,
    sex INT NOT NULL,
    cp INT NOT NULL,
    trestbps INT NOT NULL,
    chol INT NOT NULL,
    fbs INT NOT NULL,
    restecg INT NOT NULL,
    thalach INT NOT NULL,
    exang INT NOT NULL,
    oldpeak FLOAT NOT NULL,
    slope INT NOT NULL,
    ca INT NOT NULL,
    thal INT NOT NULL,
    target INT NOT NULL
);