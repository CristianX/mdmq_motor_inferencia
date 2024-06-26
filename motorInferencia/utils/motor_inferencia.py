"""Evaluando frases ingresadas para calcular su certeza"""

from decouple import config
from django.core.cache import cache
from django.http import Http404
from experta import *
from mongoengine import EmbeddedDocument
from sklearn.metrics.pairwise import cosine_similarity

from motorInferencia.models import KeyWordsNoMappingModel

from .data_resultado_inferencia import DataSetResultadoInferencia
from .dataset_motor_inferencia import DataSetMotorInferencia

# pylint: disable=no-member


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


def init_motor():
    global engine, data_inferencia, keywords

    # Carga inicial del motor
    keywords = dict(DataSetMotorInferencia.get_instance())
    raw_data = DataSetResultadoInferencia.get_instance()
    print("Inicializando motor: ")

    data_inferencia = {rule: embedded_to_dict(value) for rule, value in raw_data}
    engine = InferenceEngine()
    engine.reset()


def update_data():

    print("Entrando al update")

    global engine, data_inferencia, keywords
    keywords = dict(DataSetMotorInferencia.refresh_dataset())

    raw_data = DataSetResultadoInferencia.refresh_dataset()
    data_inferencia = {rule: embedded_to_dict(value) for rule, value in raw_data}
    engine = InferenceEngine()
    engine.reset()


def obtener_accion_similar(query, threshold=float(config("PORCENTAJE_TOLERANCIA"))):
    data_keywords = cache.get("dataset_motor_inferencia")
    vectorizer = cache.get("tfidf_vectorizer")

    if not data_keywords or not vectorizer:
        raise ValueError("Keywords, actions o vectorizer no encontrados en cache")

    keywords_list = [keyword for keyword, action in data_keywords]
    actions_list = [action for keyword, action in data_keywords]

    query_vector = vectorizer.transform([query])
    keywords_vector = vectorizer.transform(keywords_list)

    cosine_similarities = cosine_similarity(query_vector, keywords_vector).flatten()

    similar_idxs = [i for i, val in enumerate(cosine_similarities) if val >= threshold]

    return [actions_list[idx] for idx in similar_idxs]


def motor_inferencia(consulta):
    global engine, data_inferencia

    if engine is None:
        init_motor()

    if (
        DataSetResultadoInferencia.data_changed()
        or DataSetMotorInferencia.data_changed()
    ):
        update_data()

    actions_vector = obtener_accion_similar(consulta)

    print("Acción sugerida: ", actions_vector)

    posible_results = {}

    for action_vector in actions_vector:
        if engine is not None:  # Agrega esta comprobación
            engine.reset()
            engine.declare(Command(action=action_vector))
            engine.run()
            for fact_key in engine.facts:
                fact = engine.facts[fact_key]
                if isinstance(fact, Resultado):
                    posible_results[action_vector] = fact["resultado"]

    if posible_results:
        return {"found": True, "resultado": posible_results}

    try:
        keyword_no_mapping = KeyWordsNoMappingModel.objects(keyword=consulta).first()

        if not keyword_no_mapping:
            keyword_no_mapping = KeyWordsNoMappingModel(
                keyword=consulta, conteo_consulta=1
            )
            keyword_no_mapping.save()
        else:
            keyword_no_mapping.conteo_consulta += 1
            keyword_no_mapping.save()

    except Exception as e:
        return {"error": f"Error en la asignación de frase: {e}", "status": 500}
    raise Http404("No se ha encontrado ningún resultado para esta búsqueda")
