# Usamos una imagen base oficial de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Copiamos el archivo requirements.txt al contenedor
COPY requirements.txt requirements.txt

# Instalamos las dependencias necesarias
#RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos de la aplicación al contenedor
COPY . .

# Exponemos el puerto en el que la aplicación Flask correrá
EXPOSE 5000

# Comando para ejecutar la aplicación Flask usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]