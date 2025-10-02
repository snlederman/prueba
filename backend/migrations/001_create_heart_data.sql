-- Archivo: 001_create_heart_data.sql

-- Creación de la tabla de staging: heart_data_staging
-- Esta tabla se utiliza para cargar los datos tal como vienen del CSV, sin restricciones de integridad
-- (se permiten NULLs y duplicados). Posteriormente se aplicarán pruebas de calidad y se migrarán solo los
-- registros válidos a la tabla de producción.
CREATE TABLE IF NOT EXISTS heart_data_staging (
    id int ,
    age int,
    sex int,
    cp int,
    trestbps int,
    chol int,
    fbs int,
    restecg int,
    thalach int,
    exang int,
    oldpeak float,
    slope int,
    ca int,
    thal int,
    targetint
);

-- Creación de la tabla de producción: heart_data
CREATE TABLE IF NOT EXISTS heart_data (
    id INT UNIQUE NOT NULL PRIMARY KEY ,
    age INT NOT NULL,
    sex INT NOT NULL CHECK (sex IN (0, 1)),
    cp INT NOT NULL CHECK (cp IN (1, 2, 3, 4)),
    trestbps INT NOT NULL,
    chol INT NOT NULL,
    fbs INT NOT NULL CHECK (fbs IN (0, 1)),
    restecg INT NOT NULL CHECK (restecg IN (0, 1, 2)),
    thalach INT NOT NULL,
    exang INT NOT NULL CHECK (exang IN (0, 1)),
    oldpeak FLOAT NOT NULL,
    slope INT NOT NULL,
    ca INT NOT NULL CHECK (ca IN (0, 1, 2, 3)),
    thal INT NOT NULL CHECK (thal IN (1, 2, 3)),
    target INT NOT NULL CHECK (target IN (0, 1))
    -- #TODO: Define la columna `id` como PRIMARY KEY.
    -- #TODO: Agrega el resto de las columnas, estableciendo NOT NULL en cada una según el Data Dictionary del CSV.
    -- #TODO: Agrega una restricción UNIQUE para evitar duplicados.
);