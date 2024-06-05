# serializers.py
from rest_framework_mongoengine import serializers

from motorInferencia.models import CatalogoGrupoFormularioModel, InferenciaModel


class CatalogoGrupoFormularioSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CatalogoGrupoFormularioModel
        fields = "__all__"


class InferenciaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = InferenciaModel
        fields = "__all__"
