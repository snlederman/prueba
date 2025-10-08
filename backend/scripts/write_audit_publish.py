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
    """Convierte el valor a entero si es posible, o retorna None para cadenas vacías."""
    return int(value) if value.strip() != "" else None


def safe_numeric(value):
    """Convierte el valor a flotante si es posible, o retorna None para cadenas vacías."""
    return float(value) if value.strip() != "" else None


def insert_into_staging():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convierte cada campo: si está vacío, utiliza None.
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

            # Inserta la fila tal como llega en staging (aquí permitimos valores NULL).
            # TODO: Define el query SQL para insertar cada fila del CSV en la tabla 'heart_data_staging'.
            #  Debes incluir todas las columnas (incluyendo 'id') en el orden del Data Dictionary y utilizar placeholders.
            query = """
                #TODO: Completar el query de inserción en heart_data_staging
            INSERT INTO heart_data (id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
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
            errors.append(f"{field} falta")

    # Verifica duplicados en 'id' usando el conjunto seen_ids.
    try:
        current_id = int(row['id'])
        if current_id in seen_ids:
            errors.append("id duplicado")
        else:
            seen_ids.add(current_id)
    except Exception:
        errors.append("El id debe ser único")

    # Numeric validations
    try:
        age = int(row['age'])
        # TODO: Define la condición para verificar que 'age' sea mayor que 0.
        if age <= 0:
            errors.append("La edad debe ser > 0")
    except Exception:
        errors.append("La edad debe ser un entero")

    try:
        trestbps = int(row['trestbps'])
        # TODO: Define la condición para verificar que 'trestbps' esté en el rango 90-200.
        if trestbps < 90 or trestbps > 200:
            errors.append("La presión arterial en reposo está fuera del rango (90-200)")
    except Exception:
        errors.append("La presión arterial en reposo debe ser un entero")

    try:
        chol = int(row['chol'])
        # TODO: Define la condición para verificar que 'chol' esté en el rango 100-600.
        if chol <100 or chol>600:
            errors.append("El colesterol está fuera del rango (100-600)")
    except Exception:
        errors.append("El colesterol debe ser un entero")

    try:
        target = int(row['target'])
        # TODO: Define la condición para verificar que 'target' solo contenga 0 o 1.
        if target not in [0,1]:
            errors.append("El target debe ser 0 o 1")
    except Exception:
        errors.append("El target debe ser un entero")

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
            print(f"Saltando la fila con id {row_dict['id']} debido al error: {errors}")
            skipped_count += 1
            continue

        # TODO: Define el query SQL para migrar los datos desde 'heart_data_staging' a 'heart_data'
        #  de forma idempotente (por ejemplo, utilizando ON CONFLICT).
        insert_query = """
            #TODO: Completar el query para insertar datos de staging en la tabla de producción.
            INSERT INTO heart_data (id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
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

    # Limpiar staging: eliminar tabla después de procesar
    # TODO: Define el query SQL para eliminar la tabla 'heart_data_staging' una vez que los datos han sido publicados.
    query_cleanup = """
        #TODO: Completar el query para eliminar la tabla de staging.
        DELETE FROM heart_data_staging;
    """
    cur.execute(query_cleanup)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Proceso de publicación completado: {valid_count} filas migradas, {skipped_count} filas omitidas, y staging limpiado.")


if __name__ == "__main__":
    print("Iniciando proceso Write – Audit – Publish...")
    insert_into_staging()
    publish_data()
    print("Proceso completado.")
