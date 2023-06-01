# Motor de inferencia con DJango

## 0. Instalación Django

- pip install Django

## 1. Para la ejecución incial del proyecto

- python manage.py migrate
- python manage.py runserver

## 2. Uso de Pylint

- pip install djangorestframework (Añadir en settings.py/ Installed APPS 'rest_framework')
- pip install markdown
- pip install django-filter
- pip install pylint-django
- Usar pylint djando con vscode files/preferences/extensions/python/ buscar pylint path y colocar ¨pylint_django¨

## 3. Uso de imagenes en migraciones

- Instalar la dependencia (pip install Pillow)

## 4. Para la migración de modelos personalizados (Existentes en app)

1. python manage.py makemigrations
<!-- Obteniendo un id de la migración Ejem. 001 -->
2. python manage.py sqlmigrate motorInferencia 001
3. python manage.py migrate

## Instalar experta

- pip install experta

(Versión compatible con python 3.8)
