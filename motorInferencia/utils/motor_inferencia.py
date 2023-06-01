from experta import *
import difflib


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
            ],
            "compra_predio",
        ),
        (
            [
                "Como obtener una licencia metropolitana urbanística",
                "sacar licencia metropolitana urbanistica",
                "que hago para sacar una licencia metropolitana",
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
    if matched_action and max_similarity >= 0.7:
        engine.reset()
        engine.declare(Command(action=matched_action))
        engine.run()

    return (
        engine.resultado
        if engine.resultado
        else "No se encontró ninguna acción correspondiente o la similitud es menor al 80%"
    )
