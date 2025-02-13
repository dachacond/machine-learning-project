# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Crear el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar solo los archivos necesarios para la API y las pruebas
COPY ./api /app/api
COPY ./models /app/models
COPY ./tests /app/tests

# Instalar dependencias necesarias
RUN pip install pytest fastapi uvicorn pandas scikit-learn joblib httpx requests

# Añadir la carpeta del proyecto al PYTHONPATH
ENV PYTHONPATH=/app

# Exponer el puerto de la API
EXPOSE 8888

# Ejecutar los Unit Tests primero para validar código sin iniciar la API
RUN pytest tests/test_main.py

# Comando final: Levantar la API y luego ejecutar los Integration Tests
CMD uvicorn api.api:app --host 0.0.0.0 --port 8888 & sleep 3 && pytest tests/integration_test.py

