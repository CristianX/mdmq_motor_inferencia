from django.core.cache import cache
from decouple import config
from .services.stl_service import STLService
from bson import ObjectId


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
            cache.set(cls._instance_key, instance, timeout=None)

        return instance

    @classmethod
    def update_instance(cls, new_inferencia_data):
        # Obtener la instancia existente
        instance = cls.get_instance()

        # Añadir nuevos datos a la instancia
        instance.append(new_inferencia_data)

        # Actualizar la instancia en la caché
        cache.set(cls._instance_key, instance, timeout=None)

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
                    "id": str(ObjectId(inferencia_resultado.id)),
                    "categoria": inferencia_resultado.categoria,
                    "nombre_tramite": inferencia_resultado.nombre_tramite,
                    "dependencia_tramite": inferencia_resultado.dependencia_tramite,
                    "url_stl": config("URL_STL")
                    + config("FICHA_TRAMITE")
                    + str(inferencia_resultado.id_tramite),
                    "url_tramite": STLService.consumo_tramite_soap(
                        inferencia_resultado.id_tramite
                    )["url_tramite"],
                    "estado": inferencia_resultado.estado,
                    "id_tramite": inferencia_resultado.id_tramite,
                    "url_redireccion": STLService.consumo_tramite_soap(
                        inferencia_resultado.id_tramite
                    )["url_redireccion"],
                    "login": STLService.consumo_tramite_soap(
                        inferencia_resultado.id_tramite
                    )["login"],
                },
            )
            if inferencia_resultado.categoria == "informacion"
            else (
                inferencia_resultado.rule.rule,
                {
                    "id": str(ObjectId(inferencia_resultado.id)),
                    "categoria": inferencia_resultado.categoria,
                    "nombre_tramite": inferencia_resultado.nombre_tramite,
                    "dependencia_tramite": inferencia_resultado.dependencia_tramite,
                    "url_pasarela_pago": config("PASARELA_PAGO"),
                    "estado": inferencia_resultado.estado,
                },
            )
            if inferencia_resultado.categoria == "pasarela_pago"
            else (
                inferencia_resultado.rule.rule,
                {
                    "id": str(ObjectId(inferencia_resultado.id)),
                    "categoria": inferencia_resultado.categoria,
                    "titulo": inferencia_resultado.titulo,
                    "descripcion": inferencia_resultado.descripcion,
                    "contactos": inferencia_resultado.contactos,
                    "correo_electronico": inferencia_resultado.correo_electronico,
                    "post_data": inferencia_resultado.post_data,
                    "estado": inferencia_resultado.estado,
                },
            )
            if inferencia_resultado.categoria == "mensaje_bienvenida"
            else (
                inferencia_resultado.rule.rule,
                {
                    "id": str(ObjectId(inferencia_resultado.id)),
                    "categoria": inferencia_resultado.categoria,
                    "nombre_formulario": inferencia_resultado.nombre_formulario,
                    "grupo_formulario": inferencia_resultado.grupo_formulario,
                    "url_formulario": inferencia_resultado.url_formulario,
                    "estado": inferencia_resultado.estado,
                },
            )
            if inferencia_resultado.categoria == "formulario"
            else (
                inferencia_resultado.rule.rule,
                {
                    "id": str(ObjectId(inferencia_resultado.id)),
                    "categoria": inferencia_resultado.categoria,
                    "titulo_pregunta": inferencia_resultado.titulo_pregunta,
                    "respuesta_pregunta": inferencia_resultado.respuesta_pregunta,
                    "estado": inferencia_resultado.estado,
                },
            )
            if inferencia_resultado.categoria == "preguntas_frecuentes"
            else None
            for inferencia_resultado in inferenciasResultadoResponse
            if inferencia_resultado.estado == "ACT"
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
            cache.set(cls._last_update_key, last_modification, timeout=None)
            return True

        return False

    @classmethod
    def refresh_dataset(cls):
        # Eliminar data de la cache
        cache.delete(cls._instance_key)

        instance = cls._create_inferencia_data()
        cache.set(cls._instance_key, instance, timeout=None)
        return instance

    @classmethod
    def remove_inference_from_cache_by_id(cls, inferencia_id):
        print("Inferencia id: ", inferencia_id)
        inferencias = cache.get(cls._instance_key)
        if inferencias:
            updated_inferencias = [
                tupla for tupla in inferencias if tupla[1]["id"] != inferencia_id
            ]

            cache.set(cls._instance_key, updated_inferencias, timeout=None)
        return updated_inferencias
