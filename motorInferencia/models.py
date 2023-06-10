# from django.db import models
from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    IntField,
    URLField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocument,
)

# Create your models here.


class RuleModel(Document):
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


class Dependencia(EmbeddedDocument):
    nombre = StringField(max_length=255)


class Instructivo(EmbeddedDocument):
    numero = IntField()
    descripcion = StringField(max_length=500)
    url = URLField()


class Prerrequisito(EmbeddedDocument):
    numero = IntField()
    descripcion = StringField(max_length=500)
    url = URLField()

    class Meta:
        abstract = True


class InferenciaModel(Document):
    rule = ReferenceField(RuleModel, reverse_delete_rule=2)
    dependencias = ListField(EmbeddedDocumentField(Dependencia))
    instructivos = ListField(EmbeddedDocumentField(Instructivo))
    prerrequisitos = ListField(EmbeddedDocumentField(Prerrequisito))
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    usuario_creacion = StringField(max_length=150, blank=False, null=False)
    dispositivo_creacion = StringField(max_length=150, blank=False, null=False)
    fecha_modificacion = DateTimeField(default=datetime.utcnow)
    usuario_modificacion = StringField(max_length=150)
    dispositivo_modificacion = StringField(max_length=150)

    def save(self, *args, **kwargs):
        self.fecha_modificacion = datetime.utcnow()
        return super(InferenciaModel, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(
            {
                "rule": self.rule,
                "dependencias": [str(dep.nombre) for dep in self.dependencias],
                "instructivos": [str(ins.descripcion) for ins in self.instructivos],
                "prerrequisitos": [str(pre.descripcion) for pre in self.prerrequisitos],
                "fecha_creacion": str(self.fecha_creacion),
                "usuario_creacion": self.usuario_creacion,
                "dispositivo_creacion": self.dispositivo_creacion,
                "fecha_modificacion": str(self.fecha_modificacion),
                "usuario_modificacion": self.usuario_modificacion,
                "dispositivo_modificacion": self.dispositivo_modificacion,
            }
        )
