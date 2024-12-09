import logging
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from typing import Dict, Any

logger = logging.getLogger(__name__)

def fit_transformers(data: pd.DataFrame, config: Dict[str, Any]) -> ColumnTransformer:
    """
    Ajusta transformadores para preprocesar datos según la configuración.
    
    Args:
        data (pd.DataFrame): Datos de entrenamiento.
        config (dict): Configuración que contiene columnas numéricas y categóricas.
    
    Returns:
        ColumnTransformer: Transformadores ajustados.
    """
    numeric_features = config['preprocessing']['numeric_features']
    categorical_features = config['preprocessing']['categorical_features']

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    logger.info("Transformadores ajustados con éxito.")
    return preprocessor


def preprocess_training_data(data: pd.DataFrame, preprocessor: ColumnTransformer) -> pd.DataFrame:
    """
    Preprocesa datos de entrenamiento usando el transformador ajustado.
    
    Args:
        data (pd.DataFrame): Datos crudos de entrenamiento.
        preprocessor (ColumnTransformer): Transformadores ajustados.
    
    Returns:
        pd.DataFrame: Datos preprocesados.
    """
    logger.info("Preprocesando datos de entrenamiento...")
    data_processed = preprocessor.fit_transform(data)
    logger.info("Datos de entrenamiento preprocesados con éxito.")
    return data_processed


def preprocess_scoring_data(data: pd.DataFrame, preprocessor: ColumnTransformer) -> pd.DataFrame:
    """
    Preprocesa datos de scoring usando transformadores previamente ajustados.
    
    Args:
        data (pd.DataFrame): Datos crudos para scoring.
        preprocessor (ColumnTransformer): Transformadores ajustados.
    
    Returns:
        pd.DataFrame: Datos preprocesados.
    """
    logger.info("Preprocesando datos de scoring...")
    data_processed = preprocessor.transform(data)
    logger.info("Datos de scoring preprocesados con éxito.")
    return data_processed
