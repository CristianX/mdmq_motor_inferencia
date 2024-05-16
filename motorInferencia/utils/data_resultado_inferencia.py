"""
Gestión de Inferencias en caché
"""
import datetime
import json

from bson import ObjectId
from decouple import config
from django.core.cache import cache

# pylint: disable=no-member


class DataSetResultadoInferencia:
    """
    Creación, actualización y eliminación de Inferencias
    """

    _instance_key = "dataset_resultado_inferencia"
    _last_update_key = "last_update_dataset_resultado_inferencia"

    @classmethod
    def get_instance(cls):
        """Obteniendo Inferencia"""
        # Verificamos si ya existe una instancia en la caché.
        instance = cache.get(cls._instance_key)

        # Si la instancia no existe, la creamos y la guardamos en la caché.
        if instance is None:
            instance = cls._create_inferencia_data()
            cache.set(cls._instance_key, instance, timeout=None)

        return instance

    @classmethod
    def update_instance(cls, new_inferencia_data):
        """Actualizando Inferencias"""
        # Obtener la instancia existente
        instance = cls.get_instance()

        # Añadir nuevos datos a la instancia
        instance.append(new_inferencia_data)

        cache.delete(cls._instance_key)

        # Actualizar la instancia en la caché
        cache.set(cls._instance_key, json.dumps(instance), timeout=None)

        return instance

    @staticmethod
    def _create_inferencia_data():
        """Creando y clasficando data de Inferencia"""
        from motorInferencia.models import InferenciaModel

        instancia_stl = json.loads(cache.get("tramites_stl"))

        InferenciaModel.ensure_indexes()

        inferencias_resultado_response = InferenciaModel.objects.all()

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
                    "url_tramite": instancia_stl.get(
                        str(inferencia_resultado.id_tramite)
                    ).get("url_tramite")
                    if instancia_stl.get(str(inferencia_resultado.id_tramite))
                    else None,
                    "estado": inferencia_resultado.estado,
                    "id_tramite": inferencia_resultado.id_tramite,
                    "url_redireccion": instancia_stl.get(
                        str(inferencia_resultado.id_tramite)
                    ).get("url_redireccion")
                    if instancia_stl.get(str(inferencia_resultado.id_tramite))
                    else None,
                    "login": instancia_stl.get(
                        str(inferencia_resultado.id_tramite)
                    ).get("login")
                    if instancia_stl.get(str(inferencia_resultado.id_tramite))
                    else None,
                    # "login": STLService.consumo_tramite_soap(
                    #     inferencia_resultado.id_tramite
                    # ).get("login")
                    # if STLService.consumo_tramite_soap(inferencia_resultado.id_tramite)
                    # else None,
                },
            )
            if inferencia_resultado.categoria == "tramite"
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
            for inferencia_resultado in inferencias_resultado_response
            if inferencia_resultado.estado == "ACT"
        ]

        return data_resultado_inferencia

    @classmethod
    def data_changed(cls):
        """Evalua si la data ha cambiado para cargarla nuevamente"""
        from motorInferencia.models import InferenciaModel

        last_modification = (
            InferenciaModel.objects.order_by("-fecha_modificacion")
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

        # if last_update is None or last_modification > last_update:
        #     cache.set(cls._last_update_key, last_modification, timeout=None)
        #     return True

        return False

    @classmethod
    def refresh_dataset(cls):
        """Refresca la data de la cache de Inferencias"""

        # Eliminar data de la cache
        cache.delete(cls._instance_key)

        instance = cls._create_inferencia_data()
        cache.set(cls._instance_key, instance, timeout=None)
        return instance

    @classmethod
    def remove_inference_from_cache_by_id(cls, inferencia_id):
        """Remueve una inferencia de la caché"""
        print("Inferencia id: ", inferencia_id)
        inferencias = cache.get(cls._instance_key)
        if inferencias:
            updated_inferencias = [
                tupla for tupla in inferencias if tupla[1]["id"] != inferencia_id
            ]

            cache.set(cls._instance_key, updated_inferencias, timeout=None)
        return updated_inferencias
