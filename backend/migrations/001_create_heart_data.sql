-- Archivo: 001_create_heart_data.sql

-- Creación de la tabla de staging: heart_data_staging
-- Esta tabla se utiliza para cargar los datos tal como vienen del CSV, sin restricciones de integridad
-- (se permiten NULLs y duplicados). Posteriormente se aplicarán pruebas de calidad y se migrarán solo los
-- registros válidos a la tabla de producción.
<<<<<<< HEAD

CREATE TABLE IF NOT EXISTS heart_data_staging  (
    id SERIAL PRIMARY KEY,
    -- Identificador único de cada registro, autoincremental
    
    age SMALLINT NOT NULL,
    -- Edad (en años). SMALLINT es suficiente.
    
    sex SMALLINT NOT NULL,
    -- Sexo (1 = masculino, 0 = femenino). SMALLINT o BOOLEAN (si solo fuera 0 o 1).
    
    cp SMALLINT NOT NULL,
    -- Tipo de dolor en el pecho (4 valores posibles). SMALLINT es apropiado.
    
    trestbps SMALLINT NOT NULL,
    -- Presión arterial en reposo (mm Hg). SMALLINT es suficiente.
    
    chol SMALLINT NOT NULL,
    -- Colesterol sérico (mg/dl). SMALLINT es suficiente.
    
    fbs SMALLINT NOT NULL,
    -- Glucosa en ayunas > 120 mg/dl (1 = verdadero, 0 = falso). SMALLINT o BOOLEAN.
    
    restecg SMALLINT NOT NULL,
    -- Resultados del electrocardiograma en reposo (valores 0, 1, 2). SMALLINT es apropiado.
    
    thalach SMALLINT NOT NULL,
    -- Frecuencia cardíaca máxima alcanzada. SMALLINT es suficiente.
    
    exang SMALLINT NOT NULL,
    -- Angina inducida por ejercicio (1 = sí, 0 = no). SMALLINT o BOOLEAN.
    
    oldpeak REAL NOT NULL,
    -- Depresión del segmento ST inducida por ejercicio. REAL para valores decimales.
    
    slope SMALLINT NOT NULL,
    -- Pendiente del segmento ST durante el ejercicio. SMALLINT es apropiado.
    
    ca SMALLINT NOT NULL,
    -- Número de vasos principales (0-3). SMALLINT es suficiente.
    
    thal SMALLINT NOT NULL,
    -- Estado de la tiroides (1 = normal; 2 = defecto fijo; 3 = defecto reversible). SMALLINT.
    
    target SMALLINT NOT NULL
    -- Variable objetivo (0 = sin enfermedad, 1 = presencia de enfermedad). SMALLINT o BOOLEAN.
=======
CREATE TABLE IF NOT EXISTS heart_data_staging (
    -- #TODO: Agrega las columnas según el Data Dictionary del CSV
>>>>>>> c74c09c17a7461041a093096b42c637a29b01ed6
);

-- Creación de la tabla de producción: heart_data
CREATE TABLE IF NOT EXISTS heart_data (
    -- #TODO: Define la columna `id` como PRIMARY KEY.
    -- #TODO: Agrega el resto de las columnas, estableciendo NOT NULL en cada una según el Data Dictionary del CSV.
    -- #TODO: Agrega una restricción UNIQUE para evitar duplicados.
<<<<<<< HEAD
);


CREATE TABLE IF NOT EXISTS heart_data (
    id SERIAL PRIMARY KEY,
    -- Identificador único de cada registro, autoincremental
    
    age SMALLINT NOT NULL,
    -- Edad (en años). SMALLINT es suficiente.
    
    sex SMALLINT NOT NULL,
    -- Sexo (1 = masculino, 0 = femenino). SMALLINT o BOOLEAN (si solo fuera 0 o 1).
    
    cp SMALLINT NOT NULL,
    -- Tipo de dolor en el pecho (4 valores posibles). SMALLINT es apropiado.
    
    trestbps SMALLINT NOT NULL,
    -- Presión arterial en reposo (mm Hg). SMALLINT es suficiente.
    
    chol SMALLINT NOT NULL,
    -- Colesterol sérico (mg/dl). SMALLINT es suficiente.
    
    fbs SMALLINT NOT NULL,
    -- Glucosa en ayunas > 120 mg/dl (1 = verdadero, 0 = falso). SMALLINT o BOOLEAN.
    
    restecg SMALLINT NOT NULL,
    -- Resultados del electrocardiograma en reposo (valores 0, 1, 2). SMALLINT es apropiado.
    
    thalach SMALLINT NOT NULL,
    -- Frecuencia cardíaca máxima alcanzada. SMALLINT es suficiente.
    
    exang SMALLINT NOT NULL,
    -- Angina inducida por ejercicio (1 = sí, 0 = no). SMALLINT o BOOLEAN.
    
    oldpeak REAL NOT NULL,
    -- Depresión del segmento ST inducida por ejercicio. REAL para valores decimales.
    
    slope SMALLINT NOT NULL,
    -- Pendiente del segmento ST durante el ejercicio. SMALLINT es apropiado.
    
    ca SMALLINT NOT NULL,
    -- Número de vasos principales (0-3). SMALLINT es suficiente.
    
    thal SMALLINT NOT NULL,
    -- Estado de la tiroides (1 = normal; 2 = defecto fijo; 3 = defecto reversible). SMALLINT.
    
    target SMALLINT NOT NULL,

    UNIQUE (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
    -- Variable objetivo (0 = sin enfermedad, 1 = presencia de enfermedad). SMALLINT o BOOLEAN.
=======
>>>>>>> c74c09c17a7461041a093096b42c637a29b01ed6
);