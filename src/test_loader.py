import yaml
from data_loader import load_training_data, load_scoring_data

# Cambiar a la ruta absoluta de config.yaml
config_path = "C:\\Users\\Daniel\\Documents\\data-science\\mle-intv-main\\src\\config.yaml"

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

