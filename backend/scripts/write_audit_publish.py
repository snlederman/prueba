write_audit_publish.py:
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
            # TODO: Define el query SQL para insertar cada fila del CSV en la tabla 'heart_data_staging'.
            #  Debes incluir todas las columnas (incluyendo 'id') en el orden del Data Dictionary y utilizar placeholders.
            query = """
                -- #TODO: Completar el query de inserción en heart_data_staging
            """
            cur.execute(query, (
                row['id'], row['age'], row['sex'], row['cp'], row['trestbps'], row['chol'],
                row['fbs'], row['restecg'], row['thalach'], row['exang'], row['oldpeak'],
                row['slope'], row['ca'], row['thal'], row['target']
            ))
            raise NotImplementedError("Implementa la inserción en 'heart_data_staging'")
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

    # Auditoría 2: Verificar que las columnas no tengan valores nulos
    query_null = """
        SELECT COUNT(*) FROM heart_data_staging
        WHERE id IS NULL OR age IS NULL OR target IS NULL;
    """
    cur.execute(query_null)
    null_count = cur.fetchone()[0]
    if null_count > 0:
        raise Exception(
            f"Se encontraron {null_count} registros con valores nulos en columnas obligatorias en la tabla de staging.")

    # Auditoría 3: Verificar que 'target' solo contenga 0 o 1
    query_target = """
        -- #TODO: Define el query para verificar que 'target' solo contenga 0 o 1.
    """
    cur.execute(query_target)
    count_target = cur.fetchone()[0]
    if count_target > 0:
        raise Exception(f"Se encontraron {count_target} registros con 'target' inválido en la tabla de staging.")

    # Auditoría 4: Verificar que 'age' sea mayor que 0
    query_age = """
        -- #TODO: Define el query para verificar que 'age' sea mayor que 0.
    """
    cur.execute(query_age)
    count_age = cur.fetchone()[0]
    if count_age > 0:
        raise Exception(f"Se encontraron {count_age} registros con 'age' inválido en la tabla de staging.")

    # Auditoría 5: Verificar que 'trestbps' esté en un rango razonable (90-200)
    query_trestbps = """
        -- #TODO: Define el query para verificar que 'trestbps' esté en el rango 90-200.
    """
    cur.execute(query_trestbps)
    count_trestbps = cur.fetchone()[0]
    if count_trestbps > 0:
        raise Exception(
            f"Se encontraron {count_trestbps} registros con 'trestbps' fuera del rango permitido (90-200) en la tabla de staging.")

    # Auditoría 6: Verificar que 'chol' esté en un rango razonable (100-600)
    query_chol = """
        -- #TODO: Define el query para verificar que 'chol' esté en el rango 100-600.
    """
    cur.execute(query_chol)
    count_chol = cur.fetchone()[0]
    if count_chol > 0:
        raise Exception(
            f"Se encontraron {count_chol} registros con 'chol' fuera del rango permitido (100-600) en la tabla de staging.")

    cur.close()
    conn.close()
    print("Auditoría de datos completada: datos válidos.")


def publish_data():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # TODO: Define el query SQL para migrar los datos desde 'heart_data_staging' a 'heart_data'
    #  de forma idempotente (por ejemplo, utilizando ON CONFLICT).
    query_insert = """
        -- #TODO: Completar el query para insertar datos de staging en la tabla de producción.
    """
    cur.execute(query_insert)
    raise NotImplementedError("Implementa la inserción desde staging a producción")

    conn.commit()

    # TODO: Define el query SQL para limpiar la tabla 'heart_data_staging' una vez que los datos han sido publicados.
    query_cleanup = """
        -- #TODO: Completar el query para limpiar la tabla de staging.
    """
    cur.execute(query_cleanup)
    raise NotImplementedError("Implementa la limpieza de la tabla de staging")

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
