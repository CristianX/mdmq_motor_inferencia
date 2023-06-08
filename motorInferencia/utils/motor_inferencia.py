from experta import *
import difflib
from decouple import config
from django.conf import settings
from .dataset_motor_inferencia import DataSetMotorInferencia


class Command(Fact):
    pass


def motor_inferencia(consulta):
    class InferenceEngine(KnowledgeEngine):
        def __init__(self):
            super().__init__()
            self.resultado = None

        @Rule(Command(action="consulta_permiso"))
        def rule_compra_predio(self):
            self.resultado = {
                "1": {
                    "descripcion": "Entrar al portal PAM",
                    "link": "https://pam.quito.gob.ec/PAM/Inicio.aspx",
                },
                "2": "Dirigirse al apartado Trámites Frecuentes",
                "3": "Seleccionar el apartado 'predios'",
            }

        @Rule(Command(action="prueba"))
        def rule_licencia_metropolitana_urbanistica(self):
            self.resultado = {
                "1": {
                    "descripcion": "Entrar al portal PAM",
                    "link": "https://pam.quito.gob.ec/PAM/Inicio.aspx",
                },
                "2": "Dirigirse al apartado Trámites Frecuentes",
                "3": "Ingresar al apartado LMU40",
            }

    # Creando instancia del motor de inferencia
    engine = InferenceEngine()

    # Obteniendo comando de entrada
    command = consulta

    keywords = DataSetMotorInferencia.get_instance()

    # Buscando palabras clave en el comando
    matched_action = None
    max_similarity = 0
    # for keyword_list, action in keywords:
    #     for keyword in keyword_list:
    #         similarity = difflib.SequenceMatcher(None, keyword, command.lower()).ratio()
    #         if similarity > max_similarity:
    #             max_similarity = similarity
    #             matched_action = action
    for keyword, action in keywords:
        similarity = difflib.SequenceMatcher(None, keyword, command.lower()).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            matched_action = action

    # Estableciendo hecho y realizando inferencia
    if matched_action and max_similarity >= float(config("PORCENTAJE_TOLERANCIA")):
        engine.reset()
        engine.declare(Command(action=matched_action))
        engine.run()

    return (
        engine.resultado
        if engine.resultado
        else "No se encontró respuesta para su solicitud, dirigirse a la url https://pam.quito.gob.ec/PAM/Inicio.aspx, al apartado de la parte inferior (Contactos)"
    )
