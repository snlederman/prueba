import React, { useState } from 'react';

function PredictionForm() {
  const [input, setInput] = useState({
    age: '',
    sex: '',
    cp: '',
    trestbps: '',
    chol: '',
    fbs: '',
    restecg: '',
    thalach: '',
    exang: '',
    oldpeak: '',
    slope: '',
    ca: '',
    thal: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/predict-rating/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input)
      });
      const data = await res.json();
      if (data.error) {
        console.error('Error from API:', data.error);
        setPrediction("Error: " + data.error);
      } else {
        setPrediction(data.predicted_rating);
      }
    } catch (error) {
      console.error('Error:', error);
      setPrediction("Error: " + error.toString());
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Edad:
          <input
            type="number"
            name="Edad"
            value={input.age}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Sexo:
          <input
            type="number"
            name="Sexo"
            value={input.sex}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        {/* #TODO: agregar el resto de las variables que hace falta */}
        <button type="submit" disabled={loading}>
          {loading ? 'Procesando...' : 'Predecir Rating'}
        </button>
      </form>
      {prediction !== null && (
        <p>Predicción: {prediction}</p>
      )}
    </div>
  );
}

export default PredictionForm;