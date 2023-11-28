import threading

from django.apps import AppConfig

from .utils.data_resultado_inferencia import DataSetResultadoInferencia
from .utils.dataset_motor_inferencia import DataSetMotorInferencia
from .utils.services.stl_service import STLService
from .utils.services.wso2_service import WSO2Service


class MotorinferenciaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "motorInferencia"

    def ready(self):
        super().ready()

        # Crear un hilo para ejecutar get_instance de forma asíncrona
        thread = threading.Thread(target=self.async_get_instance)
        thread.start()

    def async_get_instance(self):
        # WSO2Service.generar_token()
        STLService.consumo_tramite_soap()
        DataSetResultadoInferencia.get_instance()
        DataSetMotorInferencia.get_instance()
