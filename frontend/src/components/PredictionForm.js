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
        <label>
          Tipo de dolor de pecho:
          <input
            type="number"
            name="cp"
            value={input.cp}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Presion arterial en reposo:
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
          Colesterol serico:
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
          Resultados electrocardiograma en reposo:
          <input
            type="number"
            name="restecg"
            value={input.restecg}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Frecuencia cardiaca maxima:
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
          Angina inducida por ejercicio:
          <input
            type="number"
            name="exang"
            value={input.exang}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Depresion en segmento ST:
          <input
            type="number"
            name="oldpeak"
            value={input.oldpeak}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Pendiente de segmento ST:
          <input
            type="number"
            name="slope"
            value={input.slope}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Numero de vasos principales:
          <input
            type="number"
            name="ca"
            value={input.ca}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Estado de la tiroides:
          <input
            type="number"
            name="thal"
            value={input.thal}
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