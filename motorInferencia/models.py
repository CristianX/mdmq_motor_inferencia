# from django.db import models
from djongo import models

# Create your models here.


class RuleModel(models.Model):
    rule = models.CharField(max_length=500, blank=False, null=False, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.CharField(max_length=150, blank=False, null=False)
    dispositivo_creacion = models.CharField(max_length=150, blank=False, null=False)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modificacion = models.CharField(max_length=150)
    dispositivo_modificacion = models.CharField(max_length=150)


class KeywordsModel(models.Model):
    keyword = models.CharField(max_length=500, blank=False, null=False)
    rule = models.ObjectIdField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.CharField(max_length=150, blank=False, null=False)
    dispositivo_creacion = models.CharField(max_length=150, blank=False, null=False)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modificacion = models.CharField(max_length=150)
    dispositivo_modificacion = models.CharField(max_length=150)
