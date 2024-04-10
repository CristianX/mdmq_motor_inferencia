from bson import ObjectId
from rest_framework import serializers

from .models import CatalogoDependenciaModel


class CatalogoDependenciaSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre_dependencia = serializers.CharField(max_length=500)
    fecha_creacion = serializers.DateTimeField(read_only=True)
    usuario_creacion = serializers.CharField(max_length=150)
    dispositivo_creacion = serializers.CharField(max_length=150)
    fecha_modificacion = serializers.DateTimeField(read_only=True)
    usuario_modificacion = serializers.CharField(
        max_length=150, allow_blank=True, required=False
    )
    dispositivo_modificacion = serializers.CharField(
        max_length=150, allow_blank=True, required=False
    )

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de `CatalogoDependenciaModel`
        basada en los datos validados.
        """
        return CatalogoDependenciaModel(**validated_data).save()

    def update(self, instance, validated_data):
        """
        Actualiza y retorna una instancia existente de `CatalogoDependenciaModel`
        basada en los datos validados.
        """
        instance.nombre_dependencia = validated_data.get(
            "nombre_dependencia", instance.nombre_dependencia
        )
        instance.usuario_creacion = validated_data.get(
            "usuario_creacion", instance.usuario_creacion
        )
        instance.dispositivo_creacion = validated_data.get(
            "dispositivo_creacion", instance.dispositivo_creacion
        )
        instance.usuario_modificacion = validated_data.get(
            "usuario_modificacion", instance.usuario_modificacion
        )
        instance.dispositivo_modificacion = validated_data.get(
            "dispositivo_modificacion", instance.dispositivo_modificacion
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Transforma la instancia de `CatalogoDependenciaModel` en datos primitivos Python.
        """
        ret = super().to_representation(instance)
        ret["id"] = str(
            instance.id
        )  # Convierte ObjectId a string para la representación
        return ret

    def validate_nombre_dependencia(self, value):
        """
        Realiza la validación personalizada para el campo `nombre_dependencia`.
        Verifica que el valor tenga más de 5 caracteres.
        """
        if len(value) <= 5:
            raise serializers.ValidationError(
                "El nombre de la dependencia debe tener más de 5 caracteres."
            )
        return value
