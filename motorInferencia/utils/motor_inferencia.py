from experta import *
import difflib
from decouple import config


class Command(Fact):
    pass


def motor_inferencia(consulta):
    class InferenceEngine(KnowledgeEngine):
        def __init__(self):
            super().__init__()
            self.resultado = None

        @Rule(Command(action="compra_predio"))
        def rule_compra_predio(self):
            self.resultado = {
                "1": {
                    "descripcion": "Entrar al portal PAM",
                    "link": "https://pam.quito.gob.ec/PAM/Inicio.aspx",
                },
                "2": "Dirigirse al apartado Trámites Frecuentes",
                "3": "Seleccionar el apartado 'predios'",
            }

        @Rule(Command(action="licencia_metropolitana_urbanistica"))
        def rule_licencia_metropolitana_urbanistica(self):
            self.resultado = {
                "1": "Entrar al portal PAM",
                "2": "Dirigirse al apartado Trámites Frecuentes",
                "3": "Ingresar al apartado LMU40",
            }

    # Creando instancia del motor de inferencia
    engine = InferenceEngine()

    # Obteniendo comando de entrada
    command = consulta

    # Definiendo palabras clave y acciones asociadas
    keywords = [
        (
            [
                "Como puedo cambiar el nombre de un predio",
                "Como registro un predio",
                "registrar predio",
                "compre un predio",
                "tengo un predio, como puedo saber sobre este",
                "como puedo saber sobre el predio",
            ],
            "compra_predio",
        ),
        (
            [
                "Como obtener una licencia metropolitana urbanística",
                "sacar licencia metropolitana urbanistica",
                "que hago para sacar una licencia metropolitana urbanística",
            ],
            "licencia_metropolitana_urbanistica",
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
    if matched_action and max_similarity >= float(config("PORCENTAJE_TOLERANCIA")):
        engine.reset()
        engine.declare(Command(action=matched_action))
        engine.run()

    return (
        engine.resultado
        if engine.resultado
        else "Lo siento, no encontré una respuesta a tu pregunta pero mi equipo me ayudará a aprender para solucionar tus inquietudes."
    )
