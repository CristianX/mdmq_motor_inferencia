from experta import *
import difflib
from decouple import config
from django.conf import settings
from mongoengine import EmbeddedDocument
from .dataset_motor_inferencia import DataSetMotorInferencia
from .data_resultado_inferencia import DataSetResultadoInferencia
from motorInferencia.models import KeyWordsNoMappingModel


class Command(Fact):
    action = Field(str)


class Resultado(Fact):
    resultado = Field(dict)


class InferenceEngine(KnowledgeEngine):
    # @DefFacts()
    # def _initial_action(self):
    #     for rule, data in data_inferencia.items():
    #         yield Command(action=rule)

    def __init__(self):
        super().__init__()
        self.resultado = None

    @Rule(Command(action=MATCH.action))
    def capture_result(self, action):
        rule_data = data_inferencia.get(action)
        if rule_data:
            self.resultado = rule_data
            self.declare(Resultado(resultado=rule_data))


engine = None
data_inferencia = None
keywords = None


def embedded_to_dict(obj):
    if isinstance(obj, EmbeddedDocument):
        return dict(obj.to_mongo())
    elif isinstance(obj, list):
        return [embedded_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: embedded_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def update_data():
    global engine, data_inferencia, keywords
    keywords = dict(DataSetMotorInferencia.get_instance())

    raw_data = DataSetResultadoInferencia.get_instance()
    data_inferencia = {rule: embedded_to_dict(value) for rule, value in raw_data}
    engine = InferenceEngine()
    engine.reset()


def motor_inferencia(consulta):
    global engine, data_inferencia, keywords

    if (
        DataSetResultadoInferencia.data_changed()
        or DataSetMotorInferencia.data_changed()
    ):
        update_data()

    possible_actions = []
    max_similarity = 0
    for keyword, action in keywords.items():
        similarity_score = difflib.SequenceMatcher(
            None, keyword.lower(), consulta.lower()
        ).ratio()
        print("Keyword", keyword)
        print("Similaridad", similarity_score)
        if similarity_score > max_similarity:
            max_similarity = similarity_score
            possible_actions = [action]
        elif similarity_score >= float(config("PORCENTAJE_TOLERANCIA")):
            possible_actions.append(action)

    print("posibles acciones:", possible_actions)
    print("Maxima similaridad:", max_similarity)
    possible_results = {}

    for action in possible_actions:
        print("Accion: ", action)
        if action and max_similarity >= float(config("PORCENTAJE_TOLERANCIA")):
            engine.reset()
            engine.declare(Command(action=action))
            engine.run()
            for fact_key in engine.facts:
                fact = engine.facts[fact_key]
                if isinstance(fact, Resultado):
                    possible_results[action] = fact["resultado"]

    if possible_results:
        return {"found": True, "resultado": possible_results}

    else:
        try:
            keyword_no_mapping = KeyWordsNoMappingModel.objects(
                keyword=consulta
            ).first()

            if not keyword_no_mapping:
                keyword_no_mapping = KeyWordsNoMappingModel(
                    keyword=consulta, conteo_consulta=1
                )
                keyword_no_mapping.save()
            else:
                keyword_no_mapping.conteo_consulta += 1
                keyword_no_mapping.save()

        except Exception as e:
            return f"Error en la asignación de frase: {e}"

    return {
        "found": False,
        "message": "No se ha encontrado ningún resultado para esta búsqueda",
        "url": "https://pam.quito.gob.ec/PAM/Inicio.aspx",
        "contactos": "3952300",
        "ext": "20127",
    }

    # if matched_action and max_similarity >= float(config("PORCENTAJE_TOLERANCIA")):
    #     engine.reset()
    #     engine.declare(Command(action=matched_action))
    #     engine.run()
    #     for fact_key in engine.facts:
    #         fact = engine.facts[fact_key]
    #         if isinstance(fact, Resultado):
    #             return fact["resultado"]

    # else:
    #     try:
    #         keywords_no_mapping = KeyWordsNoMappingModel(
    #             keyword=consulta,
    #         )

    #         keywords_no_mapping.save()
    #     except:
    #         return "Error en la asignación de frase"

    # return "No se encontró respuesta para su solicitud, dirigirse a la url https://pam.quito.gob.ec/PAM/Inicio.aspx, al apartado de la parte inferior (Contactos)"
