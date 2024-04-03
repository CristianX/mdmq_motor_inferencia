"""Modelos de BDD MongoDB"""

# from django.db import models
from datetime import datetime

# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=no-member
from mongoengine import (
    DateTimeField,
    Document,
    DynamicDocument,
    IntField,
    ReferenceField,
    StringField,
)

# Create your models here.


class RuleModel(Document):
    """Colección de Reglas"""

    rule = StringField(max_length=500, required=True, unique=True)
    estado = StringField(max_length=3, required=True)
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
    """Colección de Frases"""

    keyword = StringField(max_length=500, required=True, unique=True)
    rule = ReferenceField(RuleModel, reverse_delete_rule=2)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    usuario_creacion = StringField(max_length=150, required=True)
    dispositivo_creacion = StringField(max_length=150, required=True)
    fecha_modificacion = DateTimeField(default=datetime.utcnow)
    usuario_modificacion = StringField(max_length=150)
    dispositivo_modificacion = StringField(max_length=150)

    meta = {
        "indexes": [
            "-fecha_modificacion",
        ]
    }

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


# Creando instancia para definir el modelo
KeywordsModel.ensure_indexes()


class InferenciaModel(DynamicDocument):
    """Colección de Inferencias"""

    rule = ReferenceField(RuleModel, reverse_delete_rule=2, required=True)

    estado = StringField(max_length=3, required=True)
    categoria = StringField(max_length=20)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    usuario_creacion = StringField(
        max_length=150, blank=False, null=False, required=True
    )
    dispositivo_creacion = StringField(
        max_length=150, blank=False, null=False, required=True
    )
    fecha_modificacion = DateTimeField(default=datetime.utcnow)
    usuario_modificacion = StringField(max_length=150)
    dispositivo_modificacion = StringField(max_length=150)

    meta = {"indexes": [{"fields": ["rule"], "unique": True}, "-fecha_modificacion"]}

    def save(self, *args, **kwargs):
        self.fecha_modificacion = datetime.utcnow()
        return super(InferenciaModel, self).save(*args, **kwargs)


InferenciaModel.ensure_indexes()


class KeyWordsNoMappingModel(Document):
    """Colección de Frases no Mapeadas"""

    keyword = StringField(max_length=500, required=True, unique=True)
    conteo_consulta = IntField()
    fecha_creacion = DateTimeField(default=datetime.utcnow)

    def __str__(self) -> str:
        return str(
            {
                "id": str(self.id),
                "keyword": self.keyword,
                "conteo_consulta": self.conteo_consulta,
                "fecha_creacion": str(self.fecha_creacion),
            }
        )


class CatalogoDependenciasModel(Document):
    """Colección de catálogo de dependencias"""

    nombre_dependencia = StringField(max_length=500, required=True, unique=True)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    usuario_creacion = StringField(
        max_length=150, blank=False, null=False, required=True
    )
    dispositivo_creacion = StringField(
        max_length=150, blank=False, null=False, required=True
    )
    fecha_modificacion = DateTimeField(default=datetime.utcnow)
    usuario_modificacion = StringField(max_length=150)
    dispositivo_modificacion = StringField(max_length=150)

    meta = {
        "indexes": [
            "-fecha_modificacion",
        ]
    }

    def save(self, *args, **kwargs):
        self.fecha_modificacion = datetime.utcnow()
        return super(CatalogoDependenciasModel, self).save(*args, **kwargs)


CatalogoDependenciasModel.ensure_indexes()
