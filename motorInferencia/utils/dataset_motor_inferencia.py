from django.core.cache import cache


class DataSetMotorInferencia:
    _instance_key = "dataset_motor_inferencia"
    _last_update_key = "last_update_dataset_motor_inferencia"

    @classmethod
    def get_instance(cls):
        # Verificamos si ya existe una instancia en la caché.
        instance = cache.get(cls._instance_key)

        # Si la instancia no existe, la creamos y la guardamos en la caché.
        if instance is None:
            instance = cls._create_keywords_data()
            cache.set(cls._instance_key, instance)

        return instance

    @classmethod
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

        KeywordsModel.ensure_indexes()

        keywordsResponse = KeywordsModel.objects.all()

        # Asignando data a instancia por primera vez
        data_keywords = [
            (keyword.keyword, keyword.rule.rule) for keyword in keywordsResponse
        ]
        return data_keywords
    
    @classmethod
    def data_changed(cls):
        from motorInferencia.models import KeywordsModel

        last_modification = KeywordsModel.objects.order_by('-fecha_modificacion').first().fecha_modificacion

        last_update = cache.get(cls._last_update_key)

        if last_update is None or last_modification > last_update:
            cache.set(cls._last_update_key, last_modification)
            return True
        
        return False
