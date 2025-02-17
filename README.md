# Ejercicio Integral: “Integración, Bases de Datos, ML y Dashboarding”

## Objetivo General
Demostrar habilidades en:
- Manejo de Linux y Git (incluyendo la documentación de comandos usados en la terminal)
- Creación y validación de nuevas tablas en Postgres mediante un proceso **Write – Audit – Publish**
- Población de la tabla utilizando datos de un CSV (incluido en el repositorio)
- Generación de queries y visualizaciones mediante Superset
- Implementación de un modelo predictivo de ML (usando scikit-learn) y exposición de las predicciones a través de un endpoint API, consumido en el frontend
- Despliegue completo utilizando Docker y configuración de CI/CD

> **Nota:**  
> Se debe utilizar Docker para levantar todos los servicios (base de datos, Superset, backend y frontend). Se proveen un `docker-compose.yml` y un `Makefile` con comandos preconfigurados (por ejemplo, `make up` para levantar el entorno) para que el despliegue sea reproducible.  
> Ante cualquier duda, se espera que preguntes, ya que la actitud proactiva es fundamental en nuestro entorno de trabajo.  
>  
> **Uso de Materiales Externos:**  
> Está permitido y se alienta el uso de recursos en internet, incluyendo herramientas de IA como ChatGPT, para avanzar en el ejercicio y resolver dudas. Verifica siempre el código generado para evitar errores.

---

## Data Dictionary (para el archivo heart.csv)
Todas las columnas son obligatorias y deben incluirse en la definición de la tabla:

- **id:** Identificador único de cada registro.
- **age:** Edad (en años).
- **sex:** Sexo (1 = masculino, 0 = femenino).
- **cp:** Tipo de dolor en el pecho (4 valores posibles).
- **trestbps:** Presión arterial en reposo (mm Hg).
- **chol:** Colesterol sérico (mg/dl).
- **fbs:** Glucosa en ayunas > 120 mg/dl (1 = verdadero, 0 = falso).
- **restecg:** Resultados del electrocardiograma en reposo (valores 0, 1, 2).
- **thalach:** Frecuencia cardíaca máxima alcanzada.
- **exang:** Angina inducida por ejercicio (1 = sí, 0 = no).
- **oldpeak:** Depresión del segmento ST inducida por ejercicio en comparación con el reposo.
- **slope:** Pendiente del segmento ST durante el ejercicio.
- **ca:** Número de vasos principales (0-3) coloreados por fluoroscopia.
- **thal:** Estado de la tiroides (1 = normal; 2 = defecto fijo; 3 = defecto reversible).
- **target:** Variable objetivo (usualmente 0 = sin enfermedad, 1 = presencia de enfermedad).

---

## Pasos e Instrucciones

### 1. Configuración Inicial, Linux y Git
- **Directorio de Trabajo:**  
  - En tu máquina, crea un directorio con tu nombre (por ejemplo, `proyecto_tunombre`).
  - Dentro, crea un archivo llamado `comandos_utilizados.txt` donde documentes **todos los comandos** utilizados (para crear directorios, clonar el repositorio, etc.).
  
- **Clonado del Repositorio Base:**  
  - Clona el [repositorio](https://github.com/snlederman/prueba) GitHub.  
    Este repositorio ya está configurado y contiene ejemplos de migraciones, procesos de validación y algunos endpoints de referencia, además de etiquetas `#TODO` que indican las partes que debes completar.

---

### 2. Creación y Población de Nueva Tabla en Postgres
- **Nueva Tabla:**
  - En el archivo `backend/migrations/001_create_heart_data.sql` se ha dejado incompleta la definición de las tablas. **Tú deberás completarla** de la siguiente forma:
    - **Staging:**  
      Crea la tabla `heart_data_staging` con todas las columnas indicadas en el Data Dictionary (incluyendo `id`).
    - **Producción:**  
      Crea la tabla `heart_data` con la misma estructura, estableciendo `id` como PRIMARY KEY y agregando la restricción UNIQUE.

- **Proceso Write – Audit – Publish:**  
  Este proceso se implementa en el script `backend/scripts/write_audit_publish.py` y se divide en tres partes:
  
  - **Write:**  
    - Completa el query SQL para insertar cada fila del CSV en la tabla de staging (`heart_data_staging`).  
      **[#TODO: Completa el query de inserción en 'heart_data_staging']**
  
  - **Audit:**  
    Debes implementar 6 auditorías en la tabla de staging para validar la calidad de los datos:
    - **Ejemplos ya implementados:**
      1. Verificar que no existan duplicados en la columna `id`.
      2. Verificar que las columnas obligatorias (`id`, `age` y `target`) no tengan valores nulos.
    - **Auditorías a implementar por ti:**
      3. Verificar que `target` solo contenga 0 o 1.
      4. Verificar que `age` sea mayor que 0.
      5. Verificar que `trestbps` esté en el rango 90-200.
      6. Verificar que `chol` esté en el rango 100-600.
      **[#TODO: Completa los queries SQL para las auditorías 3, 4, 5 y 6]**
  
  - **Publish:**  
    - Define el query SQL para migrar los datos desde la tabla de staging a la tabla de producción (`heart_data`) de forma idempotente (por ejemplo, utilizando ON CONFLICT).  
      **[#TODO: Completa el query SQL para insertar datos de staging en la tabla de producción de forma idempotente]**
    - Define el query SQL para limpiar la tabla de staging una vez que los datos hayan sido publicados.  
      **[#TODO: Completa el query SQL para limpiar la tabla de staging]**

---

### 3. Consultas y Visualizaciones en Superset
- **Consultas y Dashboard:**  
  - Desde SQL Lab en Superset, crea queries avanzados sobre la tabla `heart_data`:
    - “Obtener el promedio de `target` por rango de edad.”
    - “Número de registros por grupo de `cp`.”
    - **[#TODO: Completa y ajusta los queries según lo solicitado]**
  - Construye visualizaciones (gráficos de barras, líneas o pie) basadas en esos queries y agrúpalas en un dashboard.

---

### 4. Modelo Predictivo de ML y Endpoint API (Opcional – BONUS)
- **Modelo de ML:**  
  - Utilizando los datos reales de `heart_data`, implementa un modelo simple de ML con scikit-learn para predecir la variable `target` a partir de las variables independientes.  
  - En el archivo `app.py`, en la función `train_model()`, deberás:
    - Extraer los datos de la base de datos (consulta SQL)  
    - Definir X usando todas las columnas (excepto `target`)  
    - Definir y usando la columna `target`  
    - Definir el modelo a utilizar (por ejemplo, LogisticRegression())  
    **[#TODO: Completa la definición de X, y y el modelo en `train_model()`]**
  
- **Endpoint API:**  
  - El endpoint `/api/predict-rating/` ya está definido para recibir un JSON con las 13 variables y devolver la predicción.  
  - Puedes ajustar la validación de entrada o el formato de respuesta según lo consideres necesario.
  
- **Integración en Frontend:**  
  - En el archivo `frontend/src/components/PredictionForm.js`, asegúrate de que el formulario incluya los 13 campos obligatorios (según el Data Dictionary) para enviar una petición al endpoint y mostrar la predicción.
  - **[#TODO: Completa el formulario agregando los inputs faltantes]**

---

### 5. Push Final y CI/CD
- **Push Final Obligatorio:**  
  - Realiza un push de tus cambios a GitHub en una rama con el formato `nombre-apellido` y abre un Pull Request.
  
- **Pushs Intermedios:**  
  - Se valorará que realices push intermedios para que el pipeline de CI/CD (configurado en `.github/workflows/ci.yml`) verifique el avance y la calidad de la solución.
  
- **CI/CD:**  
  - El repositorio ya incluye un workflow de CI/CD que ejecuta tests (por ejemplo, para verificar la creación de las tablas y el funcionamiento del endpoint).
  - Asegúrate de que el pipeline pase sin errores.

---

## Instrucciones Finales
- **Documentación:**  
  Actualiza este README con instrucciones detalladas sobre:
  - Cómo inicializar la base de datos y crear las tablas (`heart_data_staging` y `heart_data`).
  - Cómo se ejecuta el proceso de Write – Audit – Publish.
  - Cómo levantar el entorno completo utilizando Docker (incluye el uso del Makefile y la especificación de los hosts/puertos:  
    - Base de datos: `localhost:5432`  
    - Superset: `localhost:8088`  
    - Backend: `localhost:8000`  
    - Frontend: `localhost:3000`)
  - Cómo poblar la tabla: especifica que se usó el CSV `data/heart.csv` como fuente obligatoria (la alimentación desde un API es opcional y se puede dejar como bonus).
  - Cómo consumir el endpoint de predicción (y, opcionalmente, el resumen generado por ChatGPT).
  
- **Registro de Comandos:**  
  El archivo `comandos_utilizados.txt` debe contener todos los comandos utilizados en la terminal.

- **Commits:**  
  Realiza commits parciales para documentar tu avance.

- **Entrega:**  
  Sube tus cambios a la rama `nombre-apellido` y abre un Pull Request. La integración continua evaluará los tests y la calidad general de la solución.

---

## Activación Automática de Migraciones

El entorno está configurado para que las migraciones se ejecuten automáticamente al iniciar el contenedor del backend, mediante el script `entrypoint.sh`.