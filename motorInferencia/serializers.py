# serializers.py
from rest_framework_mongoengine import serializers

from motorInferencia.models import CatalogoGrupoFormularioModel


class CatalogoGrupoFormularioSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CatalogoGrupoFormularioModel
        fields = "__all__"
