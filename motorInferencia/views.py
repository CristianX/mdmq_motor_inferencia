from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from experta import *
import difflib

class InferirConsulta(APIView):
    # Create your views here.
    def post(self, request, *args, **kwargs):

        class Command(Fact):
            action = Field(str)

        consulta = request.data

        # return Response({
        #     "message": consulta["mensaje"]
        # })

        class InferenceEngine(KnowledgeEngine):

            def __init__(self):
                self.response = None

            @Rule(Command("turn_on_light"))
            def rule_turn_on_light(self):
                self.response = Response({
                    "status": True,
                    "message": "Encendiendo la luz" 
                }, status=status.HTTP_200_OK)
            
            @Rule(Command("play_music"))
            def rule_play_music(self):
                self.response = Response({
                    "status": True,
                    "message": "Reproduciendo música"
                }, status=status.HTTP_200_OK)

        # Creando instancia del motor de inferencia
        engine = InferenceEngine()

        command = consulta["mensaje"]

        # Definiendo palabras clave y acciones asociadas
        keywords = [
            (["Prende la luz", "enciende la luz", "activa la luz"], "turn_on_light"),
            (
                [
                    "Reproduce musica",
                    "reproduce una cancion",
                    "encuentra cancion a reproducir",
                ],
                "play_music",
            ),
        ]

        # Buscando palabras clave en el comando
        matched_action = None
        max_similarity = 0
        for keyword_list, action in keywords:
            for keyword in keyword_list:
                similarity = difflib.SequenceMatcher(None, keyword, command.lower()).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    matched_action = action

        # Estableciendo hecho y realizando inferencia
        if matched_action and max_similarity >= 0.8:
            engine.declare(Command(matched_action))
            engine.run()

            if engine.response is not None:
                return engine.response
            else:
                return Response({
                    "status": False,
                    "message": "No se encontró ninguna acción asociada a la consulta"
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({
                "status": False,
                "message": "No se encontró ninguna acción asociada a la consulta"
            }, status=status.HTTP_400_BAD_REQUEST)