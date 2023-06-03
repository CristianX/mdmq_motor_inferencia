from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils.motor_inferencia import motor_inferencia
from motorInferencia.models import RuleModel, KeywordsModel


class InferirConsulta(APIView):
    # Create your views here.
    def post(self, request, *args, **kwargs):
        consulta = request.data

        try:
            response_motor_inferencia = motor_inferencia(consulta=consulta["mensaje"])
            return Response(
                {
                    "data": response_motor_inferencia,
                },
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                "La consulta a enviar debe contener el campo 'mensaje'",
                status=status.HTTP_400_BAD_REQUEST,
            )


class Rule(APIView):
    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            rule = RuleModel.objects.create(
                rule=body.get("rule"),
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
            )
            print(f"exeption: {rule}")
            return Response(
                {"message": "Regla creada exitosamente"},
                status=status.HTTP_201_CREATED,
            )

        except:
            return Response(
                {"message": "Error en la creación de la nueva regla"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Keyword(APIView):
    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            keyword = KeywordsModel.objects.create(
                keyword=body.get("keyword"),
                rule=body.get("rule"),
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
            )
            return Response(
                {"message": "Keyword creada exitosamente"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(f"exception: {e}")
            return Response(
                {"message": "Error en la creación de la nueva keyword"},
                status=status.HTTP_400_BAD_REQUEST,
            )

# TODO: analizar el cambio de Djongo a Mongoengine