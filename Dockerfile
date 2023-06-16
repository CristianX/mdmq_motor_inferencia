# Dockerfile

# Establecer la imagen base
FROM python:3.8

# Establecer variables de entorno
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Establecer el directorio de trabajo
WORKDIR /code

# Instalar dependencias
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copiar el proyecto
COPY . /code/
