from django.core.cache import cache

# from background_task import background

# Singleton motor de inferencia

# def get_keywords():
#     keywordsResponse = KeywordsModel.objects.all()
#     data_keywords = []
#     for keyword in keywordsResponse:
#         data_keywords.append((keyword.keyword, keyword.rule.rule))

#     return data_keywords


# def set_keywords():
#     # keywordsResponse = KeywordsModel.objects.all()
#     # data_keywords = []
#     # for keyword in keywordsResponse:
#     #     data_keywords.append((keyword.keyword, keyword.rule.rule))

#     return


class DataSetMotorInferencia:
    _instance_key = "dataset_motor_inferencia"

    @classmethod
    def get_instance(cls):
        from motorInferencia.models import KeywordsModel

        # Verificamos si ya existe una instancia en la caché.
        instance = cache.get(cls._instance_key)

        # Si la instancia no existe, la creamos y la guardamos en la caché.
        if instance is None:
            instance = cls._create_keywords_data()
            cache.set(cls._instance_key, instance)

        return instance

    @classmethod
    # @background(schedule=10)
    def update_instance(cls, new_keyword_data):
        # Obtener la instancia existente
        instance = cls.get_instance()

        # Añadir nuevos datos a la instancia
        instance.append(new_keyword_data)

        # Actualizar la instancia en la caché
        cache.set(cls._instance_key, instance)

        return instance

    @staticmethod
    def _create_keywords_data():
        from motorInferencia.models import KeywordsModel

        keywordsResponse = KeywordsModel.objects.all()

        # Asignando data a instancia por primera vez
        data_keywords = [
            (keyword.keyword, keyword.rule.rule) for keyword in keywordsResponse
        ]
        return data_keywords
