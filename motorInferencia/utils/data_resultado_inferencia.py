from django.core.cache import cache
from decouple import config
from .stl_service import STLService


class DataSetResultadoInferencia:
    _instance_key = "dataset_resultado_inferencia"
    _last_update_key = "last_update_dataset_resultado_inferencia"

    @classmethod
    def get_instance(cls):
        # Verificamos si ya existe una instancia en la caché.
        instance = cache.get(cls._instance_key)

        # Si la instancia no existe, la creamos y la guardamos en la caché.
        if instance is None:
            instance = cls._create_inferencia_data()
            cache.set(cls._instance_key, instance)

        return instance

    @classmethod
    def update_instance(cls, new_inferencia_data):
        # Obtener la instancia existente
        instance = cls.get_instance()

        # Añadir nuevos datos a la instancia
        instance.append(new_inferencia_data)

        # Actualizar la instancia en la caché
        cache.set(cls._instance_key, instance)

        return instance

    @staticmethod
    def _create_inferencia_data():
        from motorInferencia.models import InferenciaModel

        InferenciaModel.ensure_indexes()

        inferenciasResultadoResponse = InferenciaModel.objects.all()

        # Asignando data a instancia por primera vez
        data_resultado_inferencia = [
            (
                inferencia_resultado.rule.rule,
                {
                    "categoria": inferencia_resultado.categoria,
                    "nombre_tramite": inferencia_resultado.nombre_tramite,
                    "dependencia_tramite": inferencia_resultado.dependencia_tramite,
                    "url_stl": config("URL_STL") + inferencia_resultado.url_stl,
                    "url_tramite": STLService.consumo_tramite_soap(
                        inferencia_resultado.id_tramite
                    ),
                    "estado": inferencia_resultado.estado,
                },
            )
            for inferencia_resultado in inferenciasResultadoResponse
        ]

        return data_resultado_inferencia

    @classmethod
    def data_changed(cls):
        from motorInferencia.models import InferenciaModel

        last_modification = (
            InferenciaModel.objects.order_by("-fecha_modificacion")
            .first()
            .fecha_modificacion
        )

        last_update = cache.get(cls._last_update_key)

        if last_update is None or last_modification > last_update:
            cache.set(cls._last_update_key, last_modification)
            return True

        return False

    @classmethod
    def refresh_dataset(cls):
        # Eliminar data de la cache
        cache.delete(cls._instance_key)

        instance = cls._create_inferencia_data()
        cache.set(cls._instance_key, instance)
        return instance
