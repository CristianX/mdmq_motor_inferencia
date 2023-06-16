# Motor de inferencia con DJango

## 0. Instalación Django

- pip install Django

## 1. Para la ejecución incial del proyecto

- python manage.py migrate
- python manage.py runserver
  (para ejecutar en la red local)
- python manage.py runserver 0.0.0.0:8000 y registrar la ip o domino en settings.py/ALLOWED_HOSTS

## 2. Dependencias

- pip install djangorestframework (Añadir en settings.py/ Installed APPS 'rest_framework')
- pip install markdown
- pip install django-filter
- pip install pylint-django
- Usar pylint django con vscode files/preferences/extensions/python/ buscar pylint path y colocar ¨pylint_django¨
- pip install python-decouple (Para desacoplamiento, uso de variables de entorno)
- pip install djongo
- pip install mongoengine
- pip install pymongo==3.12.1
- pip install django-cors-headers
- pip install django-background-task

## 3. Uso de imagenes en migraciones

- Instalar la dependencia (pip install Pillow)

## 4. Para la migración de modelos personalizados (Existentes en app)

1. python manage.py makemigrations
<!-- Obteniendo un id de la migración Ejem. 001 -->
2. python manage.py sqlmigrate motorInferencia 001
3. python manage.py migrate

## Instalar experta

- pip install experta

## Instalar el requeriments.txt

- pip freeze > requirements.txt (Esto tomará todas las dependencias que se tiene en el entorno)

(Versión compatible con python 3.8)
