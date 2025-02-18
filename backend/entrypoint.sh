#!/bin/sh
set -e

echo "Waiting for Postgres to be ready..."
# Wait until PostgreSQL is accepting connections
until pg_isready -h postgres -U user; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing migrations..."
export PGPASSWORD=password
psql -h postgres -U user -d mydb -f migrations/001_create_heart_data.sql

echo "Ejecutando proceso Write – Audit – Publish..."
python scripts/write_audit_publish.py

echo "Iniciando la aplicación..."
exec python app.py