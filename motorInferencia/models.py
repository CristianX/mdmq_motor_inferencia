# from django.db import models
from djongo import models

# Create your models here.


class Keywords(models.Model):
    keyword = models.CharField(max_length=500)
    rule = models.ObjectIdField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.CharField(max_length=150)
    dispositivo_creacion = models.CharField(max_length=150)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modificacion = models.CharField(max_length=150)
    dispositivo_modificacion = models.CharField(max_length=150)


class RuleModel(models.Model):
    rule = models.CharField(max_length=500, blank=False, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.CharField(max_length=150)
    dispositivo_creacion = models.CharField(max_length=150)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modificacion = models.CharField(max_length=150)
    dispositivo_modificacion = models.CharField(max_length=150)
