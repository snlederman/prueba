-- Archivo: 001_create_heart_data.sql

-- Creación de la tabla de staging: heart_data_staging
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
CREATE TABLE IF NOT EXISTS heart_data (
    id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    sex INTEGER NOT NULL,
    cp INTEGER NOT NULL,
    trestbps INTEGER NOT NULL,
    chol INTEGER NOT NULL,
    fbs INTEGER NOT NULL,
    restecg INTEGER NOT NULL,
    thalach INTEGER NOT NULL,
    exang INTEGER NOT NULL,
    oldpeak NUMERIC NOT NULL,
    slope INTEGER NOT NULL,
    ca INTEGER NOT NULL,
    thal INTEGER NOT NULL,
    target INTEGER NOT NULL,
    UNIQUE (id)
);