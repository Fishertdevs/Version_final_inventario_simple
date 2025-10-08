# Dockerfile para Sistema de Gestión de Inventarios
# Utiliza Python 3.11 como base para ejecutar la aplicación Eel

# Imagen base oficial de Python 3.11 slim (más ligera)
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY . .

# Crear directorio para la base de datos si no existe
RUN mkdir -p /app/data

# Exponer el puerto 5000 donde corre la aplicación
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=5000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
