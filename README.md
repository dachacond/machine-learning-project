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
