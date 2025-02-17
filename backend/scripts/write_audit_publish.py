#!/usr/bin/env python3
"""
Script para ejecutar el proceso Write – Audit – Publish:
- Inserta datos en la tabla de staging.
- Aplica auditorías de calidad (utilizando queries SQL).
- Inserta de forma idempotente en la tabla de producción y limpia la staging table.
"""

import psycopg2
import csv
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'heart.csv')

def insert_into_staging():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Query para insertar cada fila en la tabla 'heart_data_staging'
            query = """
                INSERT INTO heart_data_staging (id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """
            cur.execute(query, (
                row['id'], row['age'], row['sex'], row['cp'], row['trestbps'], row['chol'],
                row['fbs'], row['restecg'], row['thalach'], row['exang'], row['oldpeak'],
                row['slope'], row['ca'], row['thal'], row['target']
            ))
    conn.commit()
    cur.close()
    conn.close()
    print("Datos insertados en staging.")

def audit_data():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Auditoría 1: Verificar duplicados en la columna 'id'
    query_dup = """
        SELECT id, COUNT(*) FROM heart_data_staging
        GROUP BY id
        HAVING COUNT(*) > 1;
    """
    cur.execute(query_dup)
    duplicates = cur.fetchall()
    if duplicates:
        raise Exception(f"Se encontraron registros duplicados en 'id' en la tabla de staging: {duplicates}")

    # Auditoría 2: Verificar que las columnas obligatorias (id, age, target) no tengan valores nulos
    query_null = """
        SELECT COUNT(*) FROM heart_data_staging
        WHERE id IS NULL OR age IS NULL OR target IS NULL;
    """
    cur.execute(query_null)
    null_count = cur.fetchone()[0]
    if null_count > 0:
        raise Exception(f"Se encontraron {null_count} registros con valores nulos en columnas obligatorias en la tabla de staging.")

    # Auditoría 3: Verificar que 'target' solo contenga 0 o 1
    query_target = """
        SELECT COUNT(*) FROM heart_data_staging
        WHERE target NOT IN (0, 1);
    """
    cur.execute(query_target)
    count_target = cur.fetchone()[0]
    if count_target > 0:
        raise Exception(f"Se encontraron {count_target} registros con 'target' inválido en la tabla de staging.")

    # Auditoría 4: Verificar que 'age' sea mayor que 0
    query_age = """
        SELECT COUNT(*) FROM heart_data_staging
        WHERE age <= 0;
    """
    cur.execute(query_age)
    count_age = cur.fetchone()[0]
    if count_age > 0:
        raise Exception(f"Se encontraron {count_age} registros con 'age' inválido en la tabla de staging.")

    # Auditoría 5: Verificar que 'trestbps' esté en el rango 90-200
    query_trestbps = """
        SELECT COUNT(*) FROM heart_data_staging
        WHERE trestbps NOT BETWEEN 90 AND 200;
    """
    cur.execute(query_trestbps)
    count_trestbps = cur.fetchone()[0]
    if count_trestbps > 0:
        raise Exception(f"Se encontraron {count_trestbps} registros con 'trestbps' fuera del rango permitido (90-200) en la tabla de staging.")

    # Auditoría 6: Verificar que 'chol' esté en el rango 100-600
    query_chol = """
        SELECT COUNT(*) FROM heart_data_staging
        WHERE chol NOT BETWEEN 100 AND 600;
    """
    cur.execute(query_chol)
    count_chol = cur.fetchone()[0]
    if count_chol > 0:
        raise Exception(f"Se encontraron {count_chol} registros con 'chol' fuera del rango permitido (100-600) en la tabla de staging.")

    cur.close()
    conn.close()
    print("Auditoría de datos completada: datos válidos.")

def publish_data():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # Query para migrar datos de staging a producción de forma idempotente
    query_insert = """
        INSERT INTO heart_data (id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
        SELECT id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target
        FROM heart_data_staging
        ON CONFLICT (id) DO NOTHING;
    """
    cur.execute(query_insert)
    conn.commit()

    # Query para limpiar la tabla de staging
    query_cleanup = """
        DELETE FROM heart_data_staging;
    """
    cur.execute(query_cleanup)
    conn.commit()
    cur.close()
    conn.close()
    print("Datos publicados en producción y staging limpiada.")

if __name__ == "__main__":
    print("Iniciando proceso Write – Audit – Publish...")
    insert_into_staging()
    audit_data()
    publish_data()
    print("Proceso completado.")