from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils.motor_inferencia import motor_inferencia


class InferirConsulta(APIView):
    # Create your views here.
    def post(self, request, *args, **kwargs):
        consulta = request.data

        response_motor_inferencia = motor_inferencia(consulta=consulta["mensaje"])
        print(response_motor_inferencia)

        return Response({
            "data": response_motor_inferencia
        })
