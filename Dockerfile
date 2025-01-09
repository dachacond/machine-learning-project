# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Crear el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY ./api /app/api
COPY ./models /app/models

# Instalar las dependencias necesarias
RUN pip install fastapi uvicorn pandas scikit-learn joblib

# Exponer el puerto 8888 para la API
EXPOSE 8888

# Comando para iniciar el servidor FastAPI
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8888"]
