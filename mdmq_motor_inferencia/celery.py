import os
from celery import Celery

# Establecer la configuración de Django para Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdmq_motor_inferencia.settings")

# Crear la instancia de Celery
app = Celery("mdmq_motor_inferencia")

# Configurar la aplicación Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodescubrir y registrar las tareas de Django en Celery
app.autodiscover_tasks()
