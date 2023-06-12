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
    tipo_requisito = StringField(max_length=255)
    url = URLField()


class DirigidoA(EmbeddedDocument):
    tipo_persona = StringField(max_length=50)
    nacionalidad = StringField(max_length=255)
    descripcion = StringField(max_length=1024)


class Horario(EmbeddedDocument):
    rango = StringField(max_length=255)
    descripcion_respuesta = StringField(max_length=1024)


class Contactos(EmbeddedDocument):
    contacto = StringField(max_length=500)
    email = StringField(max_length=200)
    telefono = StringField(max_length=300)


class BaseLegal(EmbeddedDocument):
    nombre = StringField(max_length=500)
    url = URLField()


class InferenciaModel(Document):
    rule = ReferenceField(RuleModel, reverse_delete_rule=2)
    meta = {"indexes": [{"fields": ["rule"], "unique": True}]}
    descripcion = StringField(max_length=500)
    dependencias = ListField(EmbeddedDocumentField(Dependencia))
    dirigido_a = ListField(EmbeddedDocumentField(DirigidoA))
    prerrequisitos = ListField(EmbeddedDocumentField(Prerrequisito))
    instructivos = ListField(EmbeddedDocumentField(Instructivo))
    nota = StringField(max_length=1024)
    costo_tramite = StringField(max_length=255)
    horario = EmbeddedDocumentField(Horario)
    vigencia = StringField(max_length=500)
    contactos = ListField(EmbeddedDocumentField(Contactos))
    base_legal = ListField(EmbeddedDocumentField(BaseLegal))
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
                "dependencias": [
                    str({"nombre": dep.nombre}) for dep in self.dependencias
                ],
                "dirigido_a": [
                    str(
                        {
                            "tipo_persona": dir.tipo_persona,
                            "nacionalidad": dir.nacionalidad,
                            "descripcion": dir.descripcion,
                        }
                    )
                    for dir in self.dirigido_a
                ],
                "prerrequisitos": [
                    str(
                        {
                            "numero": pre.numero,
                            "descripcion": pre.descripcion,
                            "tipo_requisito": pre.tipo_requisito,
                            "url": pre.url,
                        }
                    )
                    for pre in self.prerrequisitos
                ],
                "instructivos": [
                    str(
                        {
                            "numero": ins.numero,
                            "descripcion": ins.descripcion,
                            "url": ins.url,
                        }
                    )
                    for ins in self.instructivos
                ],
                "nota": self.nota,
                "costo_tramite": self.costo_tramite,
                "horario": str(
                    {
                        "rango": self.horario.rango,
                        "descripcion_respuesta": self.horario.descripcion_respuesta,
                    }
                ),
                "vigencia": self.vigencia,
                "contactos": [
                    str(
                        {
                            "contacto": con.contacto,
                            "email": con.email,
                            "telefono": con.telefono,
                        }
                    )
                    for con in self.contactos
                ],
                "base_legal": [
                    str({"nombre": base.nombre, "url": base.url})
                    for base in self.base_legal
                ],
                "fecha_creacion": str(self.fecha_creacion),
                "usuario_creacion": self.usuario_creacion,
                "dispositivo_creacion": self.dispositivo_creacion,
                "fecha_modificacion": str(self.fecha_modificacion),
                "usuario_modificacion": self.usuario_modificacion,
                "dispositivo_modificacion": self.dispositivo_modificacion,
            }
        )
