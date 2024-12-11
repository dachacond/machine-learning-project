import logging
import os
import yaml
import pandas as pd
import sys

# Agregar la carpeta 'src' al sistema de rutas dinámicamente
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from data_loader import load_scoring_data
from preprocessor import fit_transformers, preprocess_scoring_data

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def score_model(config_path: str) -> None:
    """
    Genera predicciones usando el modelo entrenado y los datos de scoring.

    Args:
        config_path (str): Ruta al archivo de configuración (config.yaml).
    """
    # Cargar configuración
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Cargar modelo entrenado
    model_path = config['model']['model_path']
    logger.info(f"Cargando modelo desde: {model_path}...")
    model = pd.read_pickle(model_path)

    # Cargar datos de scoring
    logger.info("Cargando datos de scoring...")
    scoring_data = load_scoring_data(config)

    # Ajustar transformadores (reutilizando configuración del entrenamiento)
    logger.info("Ajustando transformadores para datos de scoring...")
    preprocessor_path = config['model']['preprocessor_path']
    logger.info(f"Cargando preprocesador ajustado desde: {preprocessor_path}...")
    preprocessor = pd.read_pickle(preprocessor_path)

    # Preprocesar datos de scoring
    logger.info("Preprocesando datos de scoring...")
    scoring_data_processed = preprocess_scoring_data(scoring_data, preprocessor)

    # Generar predicciones
    logger.info("Generando predicciones...")
    predictions = model.predict(scoring_data_processed)

    # Guardar predicciones en un archivo CSV
    predictions_output_path = config['scoring']['predictions_output_path']
    os.makedirs(os.path.dirname(predictions_output_path), exist_ok=True)
    logger.info(f"Guardando predicciones en: {predictions_output_path}...")
    pd.DataFrame(predictions, columns=["prediction"]).to_csv(predictions_output_path, index=False)

    logger.info("Scoring completado con éxito.")

if __name__ == "__main__":
    # Ruta dinámica al archivo de configuración
    config_path = os.path.join(SRC_DIR, "config.yaml")
    score_model(config_path)
