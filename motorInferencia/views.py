from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from experta import *
import difflib
from utils.motor_inferencia import motor_inferencia

class Command(Fact):
    pass


class InferirConsulta(APIView):
    # Create your views here.
    def post(self, request, *args, **kwargs):
        consulta = request.data

        motor_inferencia(consulta=consulta["mensaje"])
