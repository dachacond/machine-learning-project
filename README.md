# README: ML Regression Logistic API with Docker

## Proyecto: Entrenamiento y Despliegue de un Modelo de Machine Learning

### Descripción del Proyecto
Este proyecto entrena un modelo de regresión logística, lo implementa en una API para scoring y lo hace reproducible mediante un contenedor Docker. La API permite preprocesar datos en formato JSON y devolver predicciones basadas en el modelo entrenado.

---

## Estructura del Proyecto

mle-intv-main/
│
├── api/
│   ├── api.py                 # Código de la API implementada con FastAPI
│
├── data/
│   ├── train.csv              # Datos de entrenamiento
│   ├── score.csv              # Datos de scoring
│
├── models/
│   ├── logistic_regression.pkl # Modelo entrenado (regresión logística)
│   ├── preprocessor.pkl       # Preprocesador ajustado
│   ├── predictions.csv        # Archivo generado con las predicciones
│
├── notebooks/
│   ├── notebook_script.py     # Script de Python con los pasos del notebook inicial
│
├── scripts/
│   ├── train.py               # Script para entrenar el modelo
│   ├── score.py               # Script para probar el modelo con datos nuevos
│
├── src/
│   ├── data_loader.py         # Código para cargar datos
│   ├── preprocessor.py        # Código para preprocesar datos
│   ├── config.yaml            # Archivo de configuración con rutas y parámetros
│
├── tests/
│   ├── test_loader.py         # Script para probar data_loader.py
│   ├── test_preprocessor.py   # Script para probar preprocessor.py
│
├── Dockerfile                 # Archivo para construir la imagen Docker
└── README.md                  # Archivo principal de documentación

---

## Etapa 1: Entrenamiento y Scoring del Modelo

### Objetivo
Preparar los datos, entrenar un modelo de regresión logística, y generar predicciones utilizando el modelo entrenado y los datos preprocesados.

### Flujo de Trabajo
1. **Carga de Datos**:
   - Archivo: `data/train.csv` para entrenamiento y `data/score.csv` para scoring.
   - Script: `data_loader.py` carga y valida los datos según las columnas esperadas configuradas en `config.yaml`.

2. **Preprocesamiento de Datos**:
   - El preprocesamiento incluye:
     - Imputación de valores faltantes.
     - Escalado de características numéricas.
     - Codificación de variables categóricas.
   - Script: `preprocessor.py` ajusta y aplica transformadores configurados.

3. **Entrenamiento del Modelo**:
   - Script: `train.py` realiza las siguientes tareas:
     - Divide los datos en conjuntos de entrenamiento y prueba.
     - Entrena un modelo de regresión logística.
     - Evalúa el modelo con métricas como `classification_report` y `roc_auc_score`.
     - Guarda el modelo entrenado y el preprocesador en la carpeta `models/`.

4. **Generación de Predicciones**:
   - Script: `score.py` realiza las siguientes tareas:
     - Carga los datos de scoring desde `data/score.csv`.
     - Utiliza el preprocesador ajustado para transformar los datos.
     - Genera predicciones utilizando el modelo entrenado.
     - Guarda las predicciones en un archivo CSV en `models/predictions.csv`.

### Archivos Clave
- **`config.yaml`**: Archivo de configuración que define rutas, columnas esperadas y parámetros del modelo.
- **`data_loader.py`**: Carga y valida los datasets para entrenamiento y scoring.
- **`preprocessor.py`**: Define el pipeline de preprocesamiento.
- **`train.py`**: Coordina el flujo completo de entrenamiento del modelo.
- **`score.py`**: Genera predicciones usando el modelo entrenado.

### Resultados
- **Modelo Entrenado**: Guardado en `models/logistic_regression.pkl`.
- **Preprocesador Ajustado**: Guardado en `models/preprocessor.pkl`.
- **Métricas de Evaluación**: Guardadas en `models/metrics.yaml`.
- **Predicciones**: Guardadas en `models/predictions.csv`.

### Ejecución de los Scripts
- **Entrenamiento del Modelo**:
  ```bash
  python scripts/train.py
```

## Etapa 2: Despliegue del Modelo
### Objetivo
Crear una API para hacer scoring con el modelo entrenado y desplegarla en un contenedor Docker.

### Pasos Clave
1. **Implementación de la API**:
   - Framework: FastAPI.
   - Archivo: `api/api.py`.
   - Endpoint principal: `/score`.

2. **Configuración de Docker**:
   - Imagen basada en `python:3.10-slim`.
   - Archivo: `Dockerfile`.
   - Construcción:
     ```bash
     docker build -t ml-scoring-api .
     ```

3. **Ejecución del Contenedor**:
   - Comando:
     ```bash
     docker run -p 8888:8888 ml-scoring-api
     ```
   - Acceso: [http://localhost:8888](http://localhost:8888).

4. **Uso de la API**:
   - Solicitudes POST al endpoint `/score` con datos en formato JSON.
   - Ejemplo de entrada:
     ```json
     {
       "data": [[1.5, 2.3, "Tuesday", 4.2, 5.1, "Oregon", "toyota"]]
     }
     ```
   - Respuesta esperada:
     ```json
     {
       "predictions": [1]
     }
     ```

---

## Pruebas y Validaciones
### Objetivo
Garantizar la calidad del código y la correcta funcionalidad de los componentes.

### Scripts de Pruebas
- `tests/test_loader.py`: Verifica la carga de datos.
- `tests/test_preprocessor.py`: Valida el preprocesamiento de datos.

---

## Configuración del Proyecto
### Archivo `config.yaml`
Define:
- Rutas para datos y modelos.
- Parámetros de preprocesamiento y entrenamiento.

---

## Dependencias
- Python 3.10
- Bibliotecas:
  - scikit-learn
  - pandas
  - FastAPI
  - uvicorn

Instalación:
```bash
pip install -r requirements.txt
