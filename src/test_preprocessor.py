import yaml
import pandas as pd
from data_loader import load_training_data
from preprocessor import fit_transformers, preprocess_training_data

# Cambiar a la ruta absoluta de config.yaml
config_path = "C:\\Users\\Daniel\\Documents\\data-science\\mle-intv-main\\src\\config.yaml"

# Cargar configuración
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Cargar datos
data = load_training_data(config)

# Ajustar transformadores
preprocessor = fit_transformers(data, config)

# Preprocesar datos de entrenamiento
data_processed = preprocess_training_data(data, preprocessor)

print("Datos preprocesados (primeras filas):")
print(data_processed[:5])  # Mostrar primeras filas del array procesado
