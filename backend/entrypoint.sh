#!/bin/sh
set -e

echo "Ejecutando migraciones..."
export PGPASSWORD=password
psql -h postgres -U user -d mydb -f migrations/001_create_heart_data.sql

echo "Ejecutando proceso Write – Audit – Publish..."
python scripts/write_audit_publish.py

echo "Iniciando la aplicación..."
exec python app.py