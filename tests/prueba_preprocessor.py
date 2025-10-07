import yaml
import os
import sys

# Agregar la carpeta 'src' al sistema de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from data_loader import load_training_data
from preprocessor import fit_transformers, preprocess_training_data

# Ruta dinámica al archivo config.yaml
config_path = os.path.join(SRC_DIR, "config.yaml")

# Cargar configuración
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Probar carga de datos
print("Cargando datos de entrenamiento...")
data = load_training_data(config)

# Ajustar transformadores
print("Ajustando transformadores...")
preprocessor = fit_transformers(data, config)

# Preprocesar datos de entrenamiento
print("Preprocesando datos de entrenamiento...")
data_processed = preprocess_training_data(data, preprocessor)

# Mostrar las primeras filas de los datos preprocesados
print("Datos preprocesados (primeras filas):")
print(data_processed[:5])
