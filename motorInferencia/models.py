# from django.db import models
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ReferenceField

# Create your models here.


class RuleModel(Document):
    # _id = models.ObjectIdField(primary_key=True, editable=False)
    # rule = models.CharField(max_length=500, blank=False, null=False, unique=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True)
    # usuario_creacion = models.CharField(max_length=150, blank=False, null=False)
    # dispositivo_creacion = models.CharField(max_length=150, blank=False, null=False)
    # fecha_modificacion = models.DateTimeField(auto_now=True)
    # usuario_modificacion = models.CharField(max_length=150)
    # dispositivo_modificacion = models.CharField(max_length=150)
    rule = StringField(max_length=500, required=True, unique=True)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    usuario_creacion = StringField(max_length=150, required=True)
    dispositivo_creacion = StringField(max_length=150, required=True)
    fecha_modificacion = DateTimeField(default=datetime.utcnow)
    usuario_modificacion = StringField(max_length=150)
    dispositivo_modificacion = StringField(max_length=150)

    def save(self, *args, **kwargs):
        self.fecha_modificacion = datetime.utcnow()
        return super(RuleModel, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(
            {
                "id": str(self.id),
                "rule": self.rule,
                # "fecha_creacion": str(self.fecha_creacion),
                # "usuario_creacion": self.usuario_creacion,
                # "dispositivo_creacion": self.dispositivo_creacion,
                # "fecha_modificacion": str(self.fecha_modificacion),
                # "usuario_modificacion": self.usuario_modificacion,
                # "dispositivo_modificacion": self.dispositivo_modificacion,
            }
        )


class KeywordsModel(Document):
    keyword = StringField(max_length=500, required=True, unique=True)
    rule = ReferenceField(RuleModel, reverse_delete_rule=2)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    usuario_creacion = StringField(max_length=150, required=True)
    dispositivo_creacion = StringField(max_length=150, required=True)
    fecha_modificacion = DateTimeField(default=datetime.utcnow)
    usuario_modificacion = StringField(max_length=150)
    dispositivo_modificacion = StringField(max_length=150)

    def save(self, *args, **kwargs):
        self.fecha_modificacion = datetime.utcnow()
        return super(KeywordsModel, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(
            {
                "id": str(self.id),
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


# class Dependencia(models.Model):
#     nombre = models.CharField(max_length=255)

#     class Meta:
#         abstract = True


# class Instructivo(models.Model):
#     numero = models.IntegerField()
#     descripcion = models.CharField(max_length=500)
#     url = models.URLField()

#     class Meta:
#         abstract = True


# class Prerrequisito(models.Model):
#     numero = models.IntegerField()
#     descripcion = models.CharField(max_length=500)
#     url = models.URLField()

#     class Meta:
#         abstract = True


# class InferenciaModel(models.Model):
#     _id = models.ObjectIdField(primary_key=True, editable=False)
#     rule = models.ForeignKey(RuleModel, on_delete=models.CASCADE)
#     dependencias = models.JSONField()
#     instructivos = models.JSONField()
#     prerrequisitos = models.JSONField()
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     usuario_creacion = models.CharField(max_length=150, blank=False, null=False)
#     dispositivo_creacion = models.CharField(max_length=150, blank=False, null=False)
#     fecha_modificacion = models.DateTimeField(auto_now=True)
#     usuario_modificacion = models.CharField(max_length=150)
#     dispositivo_modificacion = models.CharField(max_length=150)
