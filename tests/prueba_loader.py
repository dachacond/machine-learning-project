import yaml
import os
import sys

# Agregar la carpeta 'src' al sistema de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from data_loader import load_training_data, load_scoring_data

# Ruta al archivo config.yaml
config_path = os.path.join(SRC_DIR, "config.yaml")

# Cargar configuración
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Probar carga de datos de entrenamiento
print("Cargando datos de entrenamiento...")
train_data = load_training_data(config)
print(train_data.head())  # Mostrar las primeras filas del dataset de entrenamiento

# Probar carga de datos de scoring
print("\nCargando datos de scoring...")
scoring_data = load_scoring_data(config)
print(scoring_data.head())  # Mostrar las primeras filas del dataset de scoring


