import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/mydb")
SECRET_KEY = os.getenv("SECRET_KEY", "a_strong_secret_key_here")