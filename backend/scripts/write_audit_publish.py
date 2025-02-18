#!/usr/bin/env python3
"""
Script para ejecutar el proceso Write – Audit – Publish:
- Inserta datos en la tabla de staging.
- Aplica auditorías de calidad (utilizando queries SQL para auditorías globales
  y validación por fila para determinar si cada registro es válido).
- Inserta de forma idempotente en la tabla de producción solo los registros válidos
  y limpia la tabla de staging.
"""

import psycopg2
import psycopg2.extras
import csv
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'heart.csv')


def safe_int(value):
    """Converts value to int if possible, or returns None for empty strings."""
    return int(value) if value.strip() != "" else None


def safe_numeric(value):
    """Converts value to float if possible, or returns None for empty strings."""
    return float(value) if value.strip() != "" else None


def insert_into_staging():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert each field: if empty, use None.
            row_id = safe_int(row['id'])
            age = safe_int(row['age'])
            sex = safe_int(row['sex'])
            cp = safe_int(row['cp'])
            trestbps = safe_int(row['trestbps'])
            chol = safe_int(row['chol'])
            fbs = safe_int(row['fbs'])
            restecg = safe_int(row['restecg'])
            thalach = safe_int(row['thalach'])
            exang = safe_int(row['exang'])
            oldpeak = safe_numeric(row['oldpeak'])
            slope = safe_int(row['slope'])
            ca = safe_int(row['ca'])
            thal = safe_int(row['thal'])
            target = safe_int(row['target'])

            # Insert the row as it comes into staging (we allow NULLs here)
            query = """
                INSERT INTO heart_data_staging 
                (id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cur.execute(query, (
                row_id, age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                exang, oldpeak, slope, ca, thal, target
            ))
    conn.commit()
    cur.close()
    conn.close()
    print("Datos insertados en staging.")


def is_valid_row(row, seen_ids):
    """
    Valida un registro (como dict) de la tabla staging.
    Se asegura de que ningún campo obligatorio esté vacío y que ciertos valores numéricos cumplan condiciones específicas.
    También verifica si el 'id' ya se ha procesado (para detectar duplicados a nivel de CSV).
    Retorna una lista vacía si el registro es válido, o una lista de mensajes de error en caso contrario.
    """
    errors = []
    mandatory_fields = ['id', 'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    for field in mandatory_fields:
        value = row.get(field)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            errors.append(f"{field} is missing")

    # Check for duplicate 'id' using the seen_ids set.
    try:
        current_id = int(row['id'])
        if current_id in seen_ids:
            errors.append("duplicate id")
        else:
            seen_ids.add(current_id)
    except Exception:
        errors.append("id must be an integer")

    # Numeric validations
    try:
        age = int(row['age'])
        if age <= 0:
            errors.append("age must be > 0")
    except Exception:
        errors.append("age must be an integer")

    try:
        trestbps = int(row['trestbps'])
        if not (90 <= trestbps <= 200):
            errors.append("trestbps out of range (90-200)")
    except Exception:
        errors.append("trestbps must be an integer")

    try:
        chol = int(row['chol'])
        if not (100 <= chol <= 600):
            errors.append("chol out of range (100-600)")
    except Exception:
        errors.append("chol must be an integer")

    try:
        target = int(row['target'])
        if target not in (0, 1):
            errors.append("target must be 0 or 1")
    except Exception:
        errors.append("target must be an integer")

    return errors


def publish_data():
    """
    Lee cada registro de la tabla de staging, valida individualmente y
    migra a la tabla de producción sólo los registros válidos.
    Finalmente, limpia la tabla de staging.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
        SELECT id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target 
        FROM heart_data_staging;
    """)
    rows = cur.fetchall()

    valid_count = 0
    skipped_count = 0
    seen_ids = set()

    for row in rows:
        row_dict = dict(row)
        errors = is_valid_row(row_dict, seen_ids)
        if errors:
            print(f"Skipping row id {row_dict['id']} due to errors: {errors}")
            skipped_count += 1
            continue

        insert_query = """
            INSERT INTO heart_data 
            (id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        cur.execute(insert_query, (
            row_dict['id'], row_dict['age'], row_dict['sex'], row_dict['cp'],
            row_dict['trestbps'], row_dict['chol'], row_dict['fbs'], row_dict['restecg'],
            row_dict['thalach'], row_dict['exang'], row_dict['oldpeak'], row_dict['slope'],
            row_dict['ca'], row_dict['thal'], row_dict['target']
        ))
        valid_count += 1

    conn.commit()

    # Clean up staging: remove all rows after processing
    cur.execute("DELETE FROM heart_data_staging;")
    conn.commit()
    cur.close()
    conn.close()
    print(f"Publish process completed: {valid_count} rows migrated, {skipped_count} rows skipped, and staging cleared.")


if __name__ == "__main__":
    print("Iniciando proceso Write – Audit – Publish...")
    insert_into_staging()
    publish_data()
    print("Proceso completado.")