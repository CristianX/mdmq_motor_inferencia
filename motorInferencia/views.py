from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils.motor_inferencia import motor_inferencia


class InferirConsulta(APIView):
    # Create your views here.
    def post(self, request, *args, **kwargs):
        consulta = request.data

        print(consulta["mensaje"])

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
