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
    X = df.drop(columns=['target']).values
    y = df['target'].values

    model = LogisticRegression(max_iter=1000)  # Increase max_iter if needed.
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
        age = float(data.get('age', 0))
        sex = float(data.get('sex', 0))
        cp = float(data.get('cp', 0))
        trestbps = float(data.get('trestbps', 0))
        chol = float(data.get('chol', 0))
        fbs = float(data.get('fbs', 0))
        restecg = float(data.get('restecg', 0))
        thalach = float(data.get('thalach', 0))
        exang = float(data.get('exang', 0))
        oldpeak = float(data.get('oldpeak', 0))
        slope = float(data.get('slope', 0))
        ca = float(data.get('ca', 0))
        thal = float(data.get('thal', 0))

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