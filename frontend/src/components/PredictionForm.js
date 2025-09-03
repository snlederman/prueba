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
            name="age"
            value={input.age}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Sexo (1=masculino, 0=femenino):
          <input
            type="number"
            name="sex"
            value={input.sex}
            onChange={handleChange}
            min="0"
            max="1"
            required
          />
        </label>
        <br />
        <label>
          Tipo de dolor pecho (cp 0-3):
          <input
            type="number"
            name="cp"
            value={input.cp}
            onChange={handleChange}
            min="0"
            max="3"
            required
          />
        </label>
        <br />
        <label>
          Presión arterial (trestbps):
          <input
            type="number"
            name="trestbps"
            value={input.trestbps}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Colesterol (chol):
          <input
            type="number"
            name="chol"
            value={input.chol}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Glucosa ayunas (fbs 0-1):
          <input
            type="number"
            name="fbs"
            value={input.fbs}
            onChange={handleChange}
            min="0"
            max="1"
            required
          />
        </label>
        <br />
        <label>
          Electrocardiograma (restecg 0-2):
          <input
            type="number"
            name="restecg"
            value={input.restecg}
            onChange={handleChange}
            min="0"
            max="2"
            required
          />
        </label>
        <br />
        <label>
          Frecuencia cardíaca máxima (thalach):
          <input
            type="number"
            name="thalach"
            value={input.thalach}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Angina inducida (exang 0-1):
          <input
            type="number"
            name="exang"
            value={input.exang}
            onChange={handleChange}
            min="0"
            max="1"
            required
          />
        </label>
        <br />
        <label>
          Depresión ST (oldpeak):
          <input
            type="number"
            name="oldpeak"
            value={input.oldpeak}
            onChange={handleChange}
            step="0.1"
            required
          />
        </label>
        <br />
        <label>
          Pendiente ST (slope 0-2):
          <input
            type="number"
            name="slope"
            value={input.slope}
            onChange={handleChange}
            min="0"
            max="2"
            required
          />
        </label>
        <br />
        <label>
          Vasos principales (ca 0-3):
          <input
            type="number"
            name="ca"
            value={input.ca}
            onChange={handleChange}
            min="0"
            max="3"
            required
          />
        </label>
        <br />
        <label>
          Tiroides (thal 1-3):
          <input
            type="number"
            name="thal"
            value={input.thal}
            onChange={handleChange}
            min="1"
            max="3"
            required
          />
        </label>
        <br />
        <button type="submit" disabled={loading}>
          {loading ? 'Procesando...' : 'Predecir Enfermedad Cardíaca'}
        </button>
      </form>
      {prediction !== null && (
        <p>Predicción: {prediction === 1 ? 'Presencia de enfermedad' : 'Sin enfermedad'}</p>
      )}
    </div>
  );
}

export default PredictionForm;