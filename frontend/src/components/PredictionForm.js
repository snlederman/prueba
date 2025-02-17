import React, { useState } from 'react';

function PredictionForm() {
  // Inicializamos el estado con las 13 variables obligatorias
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

  // Maneja el cambio en cada input actualizando el estado
  const handleChange = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  // Maneja el envío del formulario
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
        {/* #TODO: agregar el resto de las variables que hace falta */}
        <button type="submit" disabled={loading}>
          {loading ? 'Procesando...' : 'Predecir Rating'}
        </button>
      </form>
      {prediction && <p>Predicción: {prediction}</p>}
    </div>
  );
}

export default PredictionForm;