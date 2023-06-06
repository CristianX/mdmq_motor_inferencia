# from django.db import models
from djongo import models

# Create your models here.


class RuleModel(models.Model):
    _id = models.ObjectIdField(primary_key=True, editable=False)
    rule = models.CharField(max_length=500, blank=False, null=False, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.CharField(max_length=150, blank=False, null=False)
    dispositivo_creacion = models.CharField(max_length=150, blank=False, null=False)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modificacion = models.CharField(max_length=150)
    dispositivo_modificacion = models.CharField(max_length=150)

    def __str__(self) -> str:
        return str(
            {
                "id": str(self._id),
                "rule": self.rule,
                # "fecha_creacion": str(self.fecha_creacion),
                # "usuario_creacion": self.usuario_creacion,
                # "dispositivo_creacion": self.dispositivo_creacion,
                # "fecha_modificacion": str(self.fecha_modificacion),
                # "usuario_modificacion": self.usuario_modificacion,
                # "dispositivo_modificacion": self.dispositivo_modificacion,
            }
        )


class KeywordsModel(models.Model):
    _id = models.ObjectIdField(primary_key=True, editable=False)
    keyword = models.CharField(max_length=500, blank=False, null=False, unique=True)
    rule = models.ForeignKey(RuleModel, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.CharField(max_length=150, blank=False, null=False)
    dispositivo_creacion = models.CharField(max_length=150, blank=False, null=False)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modificacion = models.CharField(max_length=150)
    dispositivo_modificacion = models.CharField(max_length=150)

    def __str__(self) -> str:
        return str(
            {
                "id": str(self._id),
                "keyword": self.keyword,
                "rule": self.rule,
                "fecha_creacion": str(self.fecha_creacion),
                "usuario_creacion": self.usuario_creacion,
                "dispositivo_creacion": self.dispositivo_creacion,
                "fecha_modificacion": str(self.fecha_modificacion),
                "usuario_modificacion": self.usuario_modificacion,
                "dispositivo_modificacion": self.dispositivo_modificacion,
            }
        )


# TODO: Está permitiendo guardar campos nulos o en blanco
