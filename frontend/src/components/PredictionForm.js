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
      setPrediction(data.predicted_rating);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Edad:
          <input type="number" name="age" value={input.age} onChange={handleChange} />
        </label>
        <br />
        <label>
          Sexo:
          <input type="number" name="sex" value={input.sex} onChange={handleChange} />
        </label>
        <br />
        <label>
          Chest Pain Type (cp):
          <input type="number" name="cp" value={input.cp} onChange={handleChange} />
        </label>
        <br />
        <label>
          Resting Blood Pressure (trestbps):
          <input type="number" name="trestbps" value={input.trestbps} onChange={handleChange} />
        </label>
        <br />
        <label>
          Cholesterol (chol):
          <input type="number" name="chol" value={input.chol} onChange={handleChange} />
        </label>
        <br />
        <label>
          Fasting Blood Sugar (fbs):
          <input type="number" name="fbs" value={input.fbs} onChange={handleChange} />
        </label>
        <br />
        <label>
          Resting ECG (restecg):
          <input type="number" name="restecg" value={input.restecg} onChange={handleChange} />
        </label>
        <br />
        <label>
          Maximum Heart Rate (thalach):
          <input type="number" name="thalach" value={input.thalach} onChange={handleChange} />
        </label>
        <br />
        <label>
          Exercise Induced Angina (exang):
          <input type="number" name="exang" value={input.exang} onChange={handleChange} />
        </label>
        <br />
        <label>
          Oldpeak:
          <input type="number" name="oldpeak" value={input.oldpeak} onChange={handleChange} />
        </label>
        <br />
        <label>
          Slope:
          <input type="number" name="slope" value={input.slope} onChange={handleChange} />
        </label>
        <br />
        <label>
          Number of Major Vessels (ca):
          <input type="number" name="ca" value={input.ca} onChange={handleChange} />
        </label>
        <br />
        <label>
          Thal:
          <input type="number" name="thal" value={input.thal} onChange={handleChange} />
        </label>
        <br />
        <button type="submit" disabled={loading}>
          {loading ? 'Procesando...' : 'Predecir Rating'}
        </button>
      </form>
      {prediction && <p>Predicción: {prediction}</p>}
    </div>
  );
}

export default PredictionForm;