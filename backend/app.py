from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# Enable CORS for all routes and allow the frontend's origin.
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
engine = create_engine(DATABASE_URL)

MODEL_PATH = "model.pkl"

def train_model():
    """
    Extract data from the 'heart_data' table and train a LogisticRegression model.
    Assumes the table has the following columns (excluding 'id'):
      age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target.
    """
    query = """
        SELECT age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target
        FROM heart_data;
    """
    df = pd.read_sql(query, engine)
    columns = ["age","sex","cp","trestbps" ,"chol","fbs","restecg","thalach","exang","oldpeak","slope","ca",
            "thal"]
    X = df[df.columns[columns]] # TODO: Usar los datos de las variables independientes de la tabla de producción (no incluir id)
    y = df[df.columns["target"]]# TODO: Usar los datos de la variable dependiente de la tabla de producción

    model = LogisticRegression()# TODO: Definir el modelo con Logistic Regression
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

if not os.path.exists(MODEL_PATH):
    model = train_model()
else:
    model = joblib.load(MODEL_PATH)

@app.route('/api/predict-rating/', methods=['POST'])
def predict_rating():
    """
    Endpoint to predict 'target' using the trained model.
    Expects a JSON with the following numeric fields:
      - age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
    """
    data = request.get_json()
    print("Received data:", data)
    try:
        # Explicitly convert each field to float (or int if preferred)
        age = int(data.get('age', 0))
        sex = int(data.get('sex', 0))
        cp = int(data.get('cp', 0))
        trestbps = int(data.get('trestbps', 0))
        chol = int(data.get('chol', 0))
        fbs = int(data.get('fbs', 0))
        restecg = int(data.get('restecg', 0))
        thalach = int(data.get('thalach', 0))
        exang = int(data.get('exang', 0))
        oldpeak = float(data.get('oldpeak', 0))
        slope = int(data.get('slope', 0))
        ca = int(data.get('ca', 0))
        thal = int(data.get('thal', 0))

        # Create a NumPy array with the converted values
        X_new = np.array([[age, sex, cp, trestbps, chol, fbs, restecg,
                            thalach, exang, oldpeak, slope, ca, thal]])
        predicted = model.predict(X_new)
        # Convert numeric prediction to a descriptive label
        if int(predicted[0]) == 0:
            result = "Sin enfermedad"
        elif int(predicted[0]) == 1:
            result = "Presencia de enfermedad"
        else:
            result = "Predicción desconocida"
        return jsonify({"predicted_rating": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)