#!/usr/bin/env python3
"""
Script para ejecutar el proceso Write – Audit – Publish:
- Inserta datos en la tabla de staging.
- Aplica auditorías de calidad.
- Inserta de forma idempotente en la tabla de producción solo los registros válidos
  y limpia la tabla de staging.
"""

import psycopg2
import psycopg2.extras
import csv
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'heart.csv')
MODEL_PATH = "model.pkl" # Ruta al modelo guardado (usado también por app.py)


def safe_int(value):
    """Convierte el valor a entero si es posible, o retorna None para cadenas vacías."""
    return int(value) if value is not None and value.strip() != "" else None


def safe_numeric(value):
    """Convierte el valor a flotante si es posible, o retorna None para cadenas vacías."""
    return float(value) if value is not None and value.strip() != "" else None


def insert_into_staging():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # Limpiar staging para idempotencia del proceso
    cur.execute("DROP TABLE IF EXISTS heart_data_staging;")
    conn.commit()
    # Se espera que las migraciones ya hayan creado heart_data_staging. 
    # Si no, esta parte fallará, lo cual es correcto.
    
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Conversión de tipos. Note que 'id' no está en el CSV original, por eso se omite.
            age = safe_int(row.get('age'))
            sex = safe_int(row.get('sex'))
            cp = safe_int(row.get('cp'))
            trestbps = safe_int(row.get('trestbps'))
            chol = safe_int(row.get('chol'))
            fbs = safe_int(row.get('fbs'))
            restecg = safe_int(row.get('restecg'))
            thalach = safe_int(row.get('thalach'))
            exang = safe_int(row.get('exang'))
            oldpeak = safe_numeric(row.get('oldpeak'))
            slope = safe_int(row.get('slope'))
            ca = safe_int(row.get('ca'))
            thal = safe_int(row.get('thal'))
            target = safe_int(row.get('target'))

            # Inserta la fila en staging. No se incluye 'id' ya que no está en el CSV original.
            query = """
                INSERT INTO heart_data_staging (
                    age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            cur.execute(query, (
                age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                exang, oldpeak, slope, ca, thal, target
            ))
    conn.commit()
    cur.close()
    conn.close()
    print("Datos insertados en staging.")


def is_valid_row(row, seen_ids):
    """
    Valida un registro de la tabla staging (paso Audit).
    Implementa las 4 auditorías requeridas.
    """
    errors = []
    
    # Auditoría 1: Campos obligatorios (Validación NULL)
    mandatory_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    for field in mandatory_fields:
        value = row.get(field)
        if value is None:
            errors.append(f"El campo '{field}' está nulo")

    # Si hay valores nulos, no se pueden hacer las validaciones numéricas, se salta el resto.
    if errors:
        return errors
    
    # Auditoría 2: age debe ser > 0
    age = row['age']
    if age <= 0:
        errors.append("La edad debe ser > 0")

    # Auditoría 3: trestbps (Presión arterial) en rango 90-200
    trestbps = row['trestbps']
    if not (90 <= trestbps <= 200):
        errors.append("La presión arterial en reposo está fuera del rango (90-200)")

    # Auditoría 4: chol (Colesterol) en rango 100-600
    chol = row['chol']
    if not (100 <= chol <= 600):
        errors.append("El colesterol está fuera del rango (100-600)")

    # Validación extra: target debe ser 0 o 1
    target = row['target']
    if target not in (0, 1):
        errors.append("El target debe ser 0 o 1")

    return errors


def train_model():
    """Entrena el modelo de Regresión Logística con los datos limpios."""
    print("Entrenando modelo de Machine Learning...")
    conn = psycopg2.connect(DATABASE_URL)
    
    # 1. Extraer los datos de la base de datos limpia
    data = pd.read_sql_query(
        "SELECT age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target FROM heart_data",
        conn
    )
    conn.close()
    
    # 2. Definir X (Características/Features)
    X = data.drop(columns=['target'])
    
    # 3. Definir y (Variable Objetivo)
    y = data['target']

    # 4. Definir y entrenar el modelo (Logistic Regression)
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X, y)
    
    # Guardar el modelo en disco para que el backend lo pueda usar
    joblib.dump(model, MODEL_PATH)
    print(f"Modelo entrenado y guardado en {MODEL_PATH}")


def publish_data():
    """
    Lee cada registro de staging, valida individualmente y migra a heart_data.
    Finalmente, limpia la tabla de staging y re-entrena el modelo ML.
    """
    conn = psycopg2.connect(DATABASE_URL)
    # Usamos DictCursor para acceder a las columnas por nombre
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Nota: Aquí la consulta no incluye 'id' porque staging no tiene un ID de secuencia.
    cur.execute("""
        SELECT age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target 
        FROM heart_data_staging;
    """)
    rows = cur.fetchall()

    valid_count = 0
    skipped_count = 0
    seen_ids = set() # No se usa 'id' del CSV, la idempotencia se basa en el UNIQUE constraint de heart_data

    for row in rows:
        row_dict = dict(row)
        # El 'id' se setea a None o 0 ya que no está en la fila de staging, se autogenerará en heart_data
        
        errors = is_valid_row(row_dict, seen_ids)
        if errors:
            skipped_count += 1
            continue

        # Query para insertar datos en la tabla de producción (heart_data) de forma idempotente.
        insert_query = """
            INSERT INTO heart_data (
                age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target
            ) VALUES (
                %(age)s, %(sex)s, %(cp)s, %(trestbps)s, %(chol)s, %(fbs)s, %(restecg)s, %(thalach)s,
                %(exang)s, %(oldpeak)s, %(slope)s, %(ca)s, %(thal)s, %(target)s
            )
            -- ON CONFLICT evita que se inserten filas con la misma combinación única de características.
            ON CONFLICT (age, sex, cp, trestbps, chol) DO NOTHING;
        """
        cur.execute(insert_query, row_dict)
        valid_count += 1

    conn.commit()

    # Limpiar staging: eliminar la tabla después de procesar
    query_cleanup = """
        DROP TABLE IF EXISTS heart_data_staging;
    """
    cur.execute(query_cleanup)
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"Proceso de publicación completado: {valid_count} filas migradas, {skipped_count} filas omitidas.")
    
    # Llama al entrenamiento del modelo después de la publicación
    train_model()


if __name__ == "__main__":
    print("Iniciando proceso Write – Audit – Publish...")
    
    # Nota: Las migraciones deben ejecutarse *antes* de este script para crear las tablas
    
    insert_into_staging()
    publish_data()
    print("Proceso completado.")