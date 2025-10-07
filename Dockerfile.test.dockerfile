# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Crear el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar solo los archivos necesarios para la API y las pruebas
# Copiar el código, modelos, tests y el archivo de dependencias
COPY ./api /app/api
COPY ./models /app/models
COPY ./tests /app/tests
COPY ./requirements.txt /app/requirements.txt

# Instalar dependencias desde requirements.txt (asegura versiones consistentes con el modelo guardado)
# y herramientas para testing (pytest, httpx, requests)
RUN pip install --no-cache-dir -r /app/requirements.txt pytest httpx requests

# Añadir la carpeta del proyecto al PYTHONPATH
ENV PYTHONPATH=/app

# Exponer el puerto de la API
EXPOSE 8888

# Ejecutar los Unit Tests primero para validar código sin iniciar la API
RUN pytest tests/test_main.py

# Comando final: Levantar la API y luego ejecutar los Integration Tests
CMD ["pytest", "tests/integration_test.py"]

