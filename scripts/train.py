import logging
import yaml
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import sys

# Agregar la carpeta 'src' al sistema de rutas dinámicamente
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from data_loader import load_training_data
from preprocessor import fit_transformers, preprocess_training_data

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def train_model(config_path: str) -> None:
    """
    Entrena un modelo de machine learning basado en los datos y la configuración.

    Args:
        config_path (str): Ruta al archivo de configuración (config.yaml).
    """
    # Cargar configuración
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Cargar datos de entrenamiento
    logger.info("Cargando datos de entrenamiento...")
    data = load_training_data(config)

    # Separar etiquetas (y) de características (X)
    target_column = config['data']['train_expected_columns'][0]  # 'y'
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    # Ajustar transformadores y preprocesar datos
    logger.info("Ajustando transformadores y preprocesando datos...")
    preprocessor = fit_transformers(data, config)
    X_processed = preprocess_training_data(X, preprocessor)

    # Guardar el preprocesador ajustado
    preprocessor_path = config['model']['preprocessor_path']
    os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
    logger.info(f"Guardando preprocesador ajustado en: {preprocessor_path}...")
    pd.to_pickle(preprocessor, preprocessor_path)

    # Dividir los datos en entrenamiento y prueba
    RANDOM_STATE = config.get('random_state', 42)
    logger.info("Dividiendo datos en entrenamiento y prueba...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=RANDOM_STATE
    )

    # Entrenar modelo
    logger.info("Entrenando modelo...")
    model = LogisticRegression(max_iter=10000, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    # Evaluar modelo
    logger.info("Evaluando modelo...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    logger.info("Generando métricas de evaluación...")
    metrics = {
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "roc_auc_score": roc_auc_score(y_test, y_pred_proba)
    }

    # Guardar métricas
    metrics_path = config['model']['metrics_path']
    logger.info(f"Guardando métricas en: {metrics_path}...")
    with open(metrics_path, "w") as f:
        yaml.dump(metrics, f)

    # Guardar modelo entrenado
    model_path = config['model']['model_path']
    logger.info(f"Guardando modelo entrenado en: {model_path}...")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    pd.to_pickle(model, model_path)

    logger.info("Entrenamiento y guardado completados con éxito.")

if __name__ == "__main__":
    # Ruta dinámica al archivo de configuración
    config_path = os.path.join(SRC_DIR, "config.yaml")
    train_model(config_path)
