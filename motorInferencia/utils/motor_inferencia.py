from experta import *
import difflib


class Command(Fact):
    pass


def motor_inferencia(consulta):


    class InferenceEngine(KnowledgeEngine):
        @Rule(Command(action="turn_on_light"))
        def rule_turn_on_light(self):
            self.declare(Fact(result="Prendiendo las luces"))

        @Rule(Command(action="play_music"))
        def rule_play_music(self):
            self.declare(Fact(result="Reproduciendo música"))


    # Creando instancia del motor de inferencia
    engine = InferenceEngine()

    # Obteniendo comando de entrada
    command = consulta

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
        engine.reset()
        engine.declare(Command(action=matched_action))
        engine.run()
        for fact in engine.facts:
            print(isinstance(fact, Fact) and hasattr(fact, "result"))
            if isinstance(fact, Fact) and hasattr(fact, "result"):
                return fact.result
            
    return "No se encontró ninguna acción correspondiente o la similitud es menor al 80%"
