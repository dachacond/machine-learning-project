import os
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializar la aplicación FastAPI
app = FastAPI(title="ML Scoring API", version="1.0")

# Cargar el modelo y el preprocesador
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/logistic_regression.pkl")
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "../models/preprocessor.pkl")

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
except Exception as e:
    raise RuntimeError(f"Error cargando el modelo o preprocesador: {e}")

# Clase para validar la entrada
class ScoringRequest(BaseModel):
    data: list[list]

# Columnas esperadas por el modelo
EXPECTED_COLUMNS = ["x1", "x2", "x3", "x4", "x5", "x6", "x7"]

# Endpoint de prueba
@app.get("/")
def read_root():
    return {"message": "API para Scoring activa"}

# Endpoint para realizar scoring
@app.post("/score")
def score(request: ScoringRequest):
    try:
        # Convertir la entrada a un DataFrame
        data_df = pd.DataFrame(request.data, columns=EXPECTED_COLUMNS)

        # Preprocesar los datos
        data_processed = preprocessor.transform(data_df)

        # Realizar predicciones
        predictions = model.predict(data_processed)

        # Devolver las predicciones
        return {"predictions": predictions.tolist()}
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=f"Error en el formato de los datos: {ve}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante el scoring: {e}"
        )
