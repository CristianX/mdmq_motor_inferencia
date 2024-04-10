"""Cache de Frases"""

import datetime

from django.core.cache import cache
from sklearn.feature_extraction.text import TfidfVectorizer

# pylint: disable=no-member

vectorizer = None


class DataSetMotorInferencia:
    """Modificación de Caché registrada de frases"""

    _instance_key = "dataset_motor_inferencia"
    _last_update_key = "last_update_dataset_motor_inferencia"

    @classmethod
    def get_instance(cls):
        """Verificando si instancia existe caso contrario se crea"""
        # Verificamos si ya existe una instancia en la caché.
        instance = cache.get(cls._instance_key)

        # Si la instancia no existe, la creamos y la guardamos en la caché.
        if instance is None:
            instance = cls._create_keywords_data()
            cache.set(cls._instance_key, instance, timeout=None)

        return instance

    @classmethod
    def update_instance(cls, new_keyword_data):
        """Actualizando instancia de caché de frases"""
        # Obtener la instancia existente
        instance = cls.get_instance()

        # Añadir nuevos datos a la instancia
        instance.append(new_keyword_data)

        cache.delete(cls._instance_key)

        # Entrenar vectorizado
        cls._train_vectorizer(instance)

        # Actualizar la instancia en la caché
        cache.set(cls._instance_key, instance, timeout=None)

        return instance

    @staticmethod
    def _create_keywords_data():
        """Guardando frases en caché"""
        global vectorizer
        from motorInferencia.models import KeywordsModel

        KeywordsModel.ensure_indexes()

        keywordsResponse = KeywordsModel.objects.all()

        # Asignando data a instancia por primera vez
        data_keywords = [
            (keyword.keyword, keyword.rule.rule) for keyword in keywordsResponse
        ]

        # Entrenando vectorizador TF-IDF
        DataSetMotorInferencia._train_vectorizer(data_keywords)

        return data_keywords

    @classmethod
    def data_changed(cls):
        """Identificando si la data ha sido cambiada para actualizar la caché"""
        from motorInferencia.models import KeywordsModel

        last_modification = (
            KeywordsModel.objects.order_by("-fecha_modificacion")
            .first()
            .fecha_modificacion
        )

        last_update = cache.get(cls._last_update_key)

        if last_update is None:
            cache.set(cls._last_update_key, last_modification, timeout=None)
            return False

        if (
            isinstance(last_update, datetime.datetime)
            and last_modification > last_update
        ):
            cache.set(cls._last_update_key, last_modification, timeout=None)
            return True

        return False

    @classmethod
    def refresh_dataset(cls):
        """Refrescando toda la data de la caché"""

        # Eliminar data de la cache
        cache.delete(cls._instance_key)
        cache.delete("tfidf_vectorizer")

        instance = cls._create_keywords_data()

        # Entrenar vectorizado
        cls._train_vectorizer(instance)

        cache.set(cls._instance_key, instance, timeout=None)
        return instance

    @classmethod
    def _train_vectorizer(cls, data_keywords):
        cache.delete("tfidf_vectorizer")
        keywords_list = [keyword for keyword, action in data_keywords]
        vectorizado = TfidfVectorizer().fit(keywords_list)
        cache.set("tfidf_vectorizer", vectorizado, timeout=None)
