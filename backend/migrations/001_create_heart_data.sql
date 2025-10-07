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
  const [error, setError] = useState(null); // Añadido manejo de errores

  const handleChange = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);
    
    // Convertir los inputs a los tipos correctos para la API (float para oldpeak, int para el resto)
    const payload = Object.keys(input).reduce((acc, key) => {
        // Aseguramos que oldpeak sea float y el resto sea int. Si el campo está vacío, enviamos 0.
        const value = input[key] === '' ? 0 : input[key];
        acc[key] = key === 'oldpeak' ? parseFloat(value) : parseInt(value, 10);
        return acc;
    }, {});

    try {
      const res = await fetch('http://localhost:8000/api/predict-rating/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      const data = await res.json();
      
      if (!res.ok || data.error) {
        // Manejar errores HTTP o errores retornados por la API
        throw new Error(data.error || `Error HTTP: ${res.status}`);
      }
      
      setPrediction(data.predicted_rating);
      
    } catch (err) {
      console.error('Error al hacer la predicción:', err);
      setError("Error al conectar con el backend o procesar la predicción. Revisa la consola y asegúrate de que el backend esté corriendo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h3>Datos del Paciente (13 Variables)</h3>

        {/* 1. age (Corregido a name="age") */}
        <label>
          Edad (años):
          <input type="number" name="age" value={input.age} onChange={handleChange} required min="1" placeholder="Ej: 52" />
        </label>
        <br />
        
        {/* 2. sex (Corregido a name="sex") */}
        <label>
          Sexo (1=Hombre, 0=Mujer):
          <input type="number" name="sex" value={input.sex} onChange={handleChange} required min="0" max="1" placeholder="Ej: 1" />
        </label>
        <br />

        {/* 3. cp (Tipo de dolor en el pecho 0-3) */}
        <label>
          Tipo de Dolor en el Pecho (cp):
          <input type="number" name="cp" value={input.cp} onChange={handleChange} required min="0" max="3" placeholder="Ej: 0" />
        </label>
        <br />
        
        {/* 4. trestbps (Presión arterial en reposo) */}
        <label>
          Presión Arterial Reposo (trestbps):
          <input type="number" name="trestbps" value={input.trestbps} onChange={handleChange} required min="90" max="200" placeholder="Ej: 130" />
        </label>
        <br />
        
        {/* 5. chol (Colesterol sérico) */}
        <label>
          Colesterol Sérico (chol):
          <input type="number" name="chol" value={input.chol} onChange={handleChange} required min="100" max="600" placeholder="Ej: 234" />
        </label>
        <br />
        
        {/* 6. fbs (Glucosa en ayunas > 120) */}
        <label>
          Glucosa Ayunas > 120 (fbs - 0/1):
          <input type="number" name="fbs" value={input.fbs} onChange={handleChange} required min="0" max="1" placeholder="Ej: 0" />
        </label>
        <br />
        
        {/* 7. restecg (Resultado del ECG 0-2) */}
        <label>
          Electrocardiograma (restecg 0-2):
          <input type="number" name="restecg" value={input.restecg} onChange={handleChange} required min="0" max="2" placeholder="Ej: 1" />
        </label>
        <br />
        
        {/* 8. thalach (Frecuencia cardíaca máxima) */}
        <label>
          Frecuencia Cardíaca Máx. (thalach):
          <input type="number" name="thalach" value={input.thalach} onChange={handleChange} required placeholder="Ej: 162" />
        </label>
        <br />
        
        {/* 9. exang (Angina inducida por ejercicio) */}
        <label>
          Angina por Ejercicio (exang - 0/1):
          <input type="number" name="exang" value={input.exang} onChange={handleChange} required min="0" max="1" placeholder="Ej: 0" />
        </label>
        <br />
        
        {/* 10. oldpeak (Depresión del segmento ST - ¡Permite decimales!) */}
        <label>
          Depresión ST (oldpeak):
          <input type="number" name="oldpeak" value={input.oldpeak} onChange={handleChange} required step="0.1" placeholder="Ej: 1.5" />
        </label>
        <br />
        
        {/* 11. slope (Pendiente del segmento ST 0-2) */}
        <label>
          Pendiente ST (slope 0-2):
          <input type="number" name="slope" value={input.slope} onChange={handleChange} required min="0" max="2" placeholder="Ej: 2" />
        </label>
        <br />
        
        {/* 12. ca (Vasos principales 0-3) */}
        <label>
          Vasos Principales (ca 0-3):
          <input type="number" name="ca" value={input.ca} onChange={handleChange} required min="0" max="3" placeholder="Ej: 0" />
        </label>
        <br />
        
        {/* 13. thal (Defecto de Talio 1/2/3) */}
        <label>
          Defecto de Talio (thal 1-3):
          <input type="number" name="thal" value={input.thal} onChange={handleChange} required min="1" max="3" placeholder="Ej: 2" />
        </label>
        <br />

        <button type="submit" disabled={loading}>
          {loading ? 'Procesando...' : 'Predecir Rating'}
        </button>
      </form>
      
      {/* Salida y manejo de errores */}
      {error && (
        <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>
      )}
      {prediction !== null && (
        <p style={{ marginTop: '10px', fontWeight: 'bold' }}>Predicción: {prediction}</p>
      )}
    </div>
  );
}

export default PredictionForm;