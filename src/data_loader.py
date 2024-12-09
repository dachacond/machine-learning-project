# data_loader.py

import logging
import pandas as pd
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

def load_training_data(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Carga el dataset de entrenamiento desde la ubicación configurada.
    
    Args:
        config (dict): Configuración que contiene la ruta del dataset de entrenamiento.
            Se asume que config['data']['train_path'] contiene el path al CSV de entrenamiento.
    
    Returns:
        pd.DataFrame: DataFrame con datos de entrenamiento.
    """
    train_path = config['data']['train_path']
    logger.info(f"Cargando datos de entrenamiento desde: {train_path}")
    df = pd.read_csv(train_path)
    validate_dataset(df, expected_columns=config['data'].get('train_expected_columns', []))
    return df


def load_scoring_data(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Carga el dataset para scoring desde la ubicación configurada.
    
    Args:
        config (dict): Configuración que contiene la ruta del dataset de scoring.
            Se asume que config['data']['scoring_path'] contiene el path al CSV de scoring.
    
    Returns:
        pd.DataFrame: DataFrame con datos para realizar predicciones.
    """
    scoring_path = config['data']['scoring_path']
    logger.info(f"Cargando datos de scoring desde: {scoring_path}")
    df = pd.read_csv(scoring_path)
    validate_dataset(df, expected_columns=config['data'].get('scoring_expected_columns', []))
    return df


def validate_dataset(df: pd.DataFrame, expected_columns: Optional[List[str]] = None) -> None:
    """
    Valida la integridad del DataFrame cargado. 
    
    Args:
        df (pd.DataFrame): DataFrame a validar.
        expected_columns (list): Lista opcional de columnas esperadas.
    
    Raises:
        ValueError: Si el DataFrame no cumple con ciertas condiciones mínimas.
    """
    if df.empty:
        logger.error("El dataset está vacío.")
        raise ValueError("El dataset cargado está vacío.")

    if expected_columns and not set(expected_columns).issubset(df.columns):
        missing = set(expected_columns) - set(df.columns)
        logger.error(f"Faltan columnas esperadas en el dataset: {missing}")
        raise ValueError(f"El dataset no contiene las columnas esperadas: {missing}")

    logger.info("El dataset ha pasado la validación correctamente.")
