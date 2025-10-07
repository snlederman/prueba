from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression 
import warnings

# Ignorar advertencias de scikit-learn
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Enable CORS para permitir la comunicación con el frontend de React
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
engine = create_engine(DATABASE_URL)

MODEL_PATH = "model.pkl"

def load_or_train_model():
    """Intenta cargar el modelo guardado; si no existe, lo entrena (solo para inicialización)."""
    if os.path.exists(MODEL_PATH):
        try:
            print("Cargando modelo existente...")
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            # Si hay un error, se carga un modelo vacío
            return LogisticRegression() 
    else:
        # Nota: El WAP se encarga del entrenamiento. Esto es un fallback.
        print("Modelo no encontrado. Se requiere ejecutar 'make run-write-audit-publish'.")
        return LogisticRegression() 

# Cargar el modelo al inicio de la aplicación
model = load_or_train_model()


@app.route('/api/predict-rating/', methods=['POST'])
def predict_rating():
    """
    Endpoint para predecir 'target' usando el modelo entrenado.
    Espera un JSON con las 13 características.
    """
    data = request.get_json()
    
    # Se espera que los 13 campos sean enviados en minúsculas y como números
    try:
        # Extraer y convertir las 13 características
        features = [
            int(data.get('age', 0)),
            int(data.get('sex', 0)),
            int(data.get('cp', 0)),
            int(data.get('trestbps', 0)),
            int(data.get('chol', 0)),
            int(data.get('fbs', 0)),
            int(data.get('restecg', 0)),
            int(data.get('thalach', 0)),
            int(data.get('exang', 0)),
            float(data.get('oldpeak', 0)), # Debe ser float
            int(data.get('slope', 0)),
            int(data.get('ca', 0)),
            int(data.get('thal', 0))
        ]
        
        # Crear un NumPy array 2D para la predicción ([1, 13])
        X_new = np.array([features])
        
        predicted = model.predict(X_new)
        
        # Convertir predicción binaria a etiqueta descriptiva
        if int(predicted[0]) == 0:
            result = "Sin enfermedad (Clase 0)"
        elif int(predicted[0]) == 1:
            result = "Presencia de enfermedad (Clase 1)"
        else:
            result = "Predicción no concluyente"
            
        return jsonify({"predicted_rating": result})
        
    except Exception as e:
        return jsonify({"error": f"Error al procesar los datos de entrada o al predecir: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)