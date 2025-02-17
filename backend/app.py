from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
engine = create_engine(DATABASE_URL)

MODEL_PATH = "model.pkl"


def train_model():
    """
    Extrae los datos de la tabla 'heart_data' y entrena un modelo de ML.
    Se asume que la tabla 'heart_data' tiene las siguientes columnas (excluyendo 'id'):
      age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target.
    TODO: Define las variables independientes X (todas las columnas excepto 'target') y la variable dependiente y (la columna 'target').
    TODO: Define el modelo a utilizar (por ejemplo, LogisticRegression).
    """
    query = """
        SELECT age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target
        FROM heart_data;
    """
    # Extraer los datos de la base de datos
    df = pd.read_sql(query, engine)

    # TODO: Define X utilizando todas las columnas en el DataFrame 'df' excepto 'target'
    X = ...

    # TODO: Define y utilizando la columna 'target' en el DataFrame 'df'
    y = ...

    # TODO: Define el modelo a utilizar, LogisticRegression()
    model = ...

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
    Endpoint para predecir la variable 'target' usando el modelo entrenado.
    Se espera que la petición POST contenga un JSON con las siguientes variables:
      - age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
    """
    data = request.get_json()
    try:
        age = data.get('age', 0)
        sex = data.get('sex', 0)
        cp = data.get('cp', 0)
        trestbps = data.get('trestbps', 0)
        chol = data.get('chol', 0)
        fbs = data.get('fbs', 0)
        restecg = data.get('restecg', 0)
        thalach = data.get('thalach', 0)
        exang = data.get('exang', 0)
        oldpeak = data.get('oldpeak', 0)
        slope = data.get('slope', 0)
        ca = data.get('ca', 0)
        thal = data.get('thal', 0)

        X_new = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        predicted = model.predict(X_new)
        return jsonify({"predicted_rating": int(predicted[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
