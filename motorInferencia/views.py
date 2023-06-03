from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils.motor_inferencia import motor_inferencia
from motorInferencia.models import RuleModel


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
            )
            return Response(
                {"message": "Regla creada exitosamente"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
