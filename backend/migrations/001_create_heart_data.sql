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
    oldpeak NUMERIC,
    slope INTEGER,
    ca INTEGER,
    thal INTEGER,
    target INTEGER
);

-- Creación de la tabla de producción: heart_data
-- La tabla de producción tiene un id como PRIMARY KEY y restricciones básicas.
CREATE TABLE IF NOT EXISTS heart_data (
    id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    sex INTEGER NOT NULL,
    cp INTEGER NOT NULL,
    trestbps INTEGER,
    chol INTEGER,
    fbs INTEGER,
    restecg INTEGER,
    thalach INTEGER,
    exang INTEGER,
    oldpeak NUMERIC,
    slope INTEGER,
    ca INTEGER,
    thal INTEGER,
    target INTEGER,
    CONSTRAINT unique_record UNIQUE (id)
);

//nota> considero innecesario que el primary key tenga un constraint U, porque al ser primary key ya es unico por definicion