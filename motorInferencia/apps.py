from django.apps import AppConfig
import threading
from .utils.dataset_motor_inferencia import DataSetMotorInferencia
from .utils.data_resultado_inferencia import DataSetResultadoInferencia


class MotorinferenciaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "motorInferencia"

    def ready(self):
        super().ready()

        # Crear un hilo para ejecutar get_instance de forma asíncrona
        thread = threading.Thread(target=self.async_get_instance)
        thread.start()

    def async_get_instance(self):
        DataSetMotorInferencia.get_instance()
        DataSetResultadoInferencia.get_instance()
