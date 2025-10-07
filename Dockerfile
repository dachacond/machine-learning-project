# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Crear el directorio de trabajo en el contenedor
WORKDIR /app

# copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt /app/requirements.txt

# instalar dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# copiar el código y modelos
COPY ./api /app/api
COPY ./models /app/models

# Exponer el puerto 8888 para la API
EXPOSE 8888

# Comando para iniciar el servidor FastAPI
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8888"]
