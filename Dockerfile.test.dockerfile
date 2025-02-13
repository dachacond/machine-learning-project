# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Crear el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar solo los archivos necesarios para la API y las pruebas
COPY ./api /app/api
COPY ./models /app/models
COPY ./tests /app/tests/test_main.py

# Instalar dependencias necesarias
RUN pip install pytest fastapi uvicorn pandas scikit-learn joblib httpx

# Añadir la carpeta del proyecto al PYTHONPATH
ENV PYTHONPATH=/app

# Comando para ejecutar pytest en la API
CMD ["pytest", "tests"]
