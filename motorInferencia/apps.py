from django.apps import AppConfig


class MotorinferenciaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "motorInferencia"

    # def ready(self):
    #     super().ready()
    #     from .utils.dataset_motor_inferencia import set_keywords

    #     set_keywords()
