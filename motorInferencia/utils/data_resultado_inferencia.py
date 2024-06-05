"""
Gestión de Inferencias en caché
"""

import datetime
import json

from bson import ObjectId
from bson.errors import InvalidId
from decouple import config
from django.core.cache import cache

from motorInferencia.models import CatalogoGrupoFormularioModel, InferenciaModel
from motorInferencia.serializers import CatalogoGrupoFormularioSerializer

# pylint: disable=no-member


class DataSetResultadoInferencia:
    """
    Creación, actualización y eliminación de Inferencias
    """

    _instance_key = "dataset_resultado_inferencia"
    _last_update_key = "last_update_dataset_resultado_inferencia"

    @staticmethod
    def obtener_grupo_formulario(grupo_formulario):
        try:
            grupo_formulario_obj = (
                CatalogoGrupoFormularioModel.objects(id=ObjectId(grupo_formulario))
                .only("nombre_grupo")
                .first()
            )

            if grupo_formulario_obj:
                return grupo_formulario_obj.nombre_grupo
            return None

        except InvalidId:
            return "id inválido"

    @classmethod
    def get_instance(cls):
        """Obteniendo Inferencia"""
        instance = cache.get(cls._instance_key)
        if instance is None:
            instance = cls._create_inferencia_data()
            cache.set(cls._instance_key, instance, timeout=None)
        return instance

    @classmethod
    def update_instance(cls, new_inferencia_data):
        """Actualizando Inferencias"""
        instance = cls.get_instance()
        instance.append(new_inferencia_data)
        cls._update_cache(instance)
        return instance

    @classmethod
    def _update_cache(cls, data):
        cache.delete(cls._instance_key)
        cache.set(cls._instance_key, data, timeout=None)

    @staticmethod
    def _create_inferencia_data():
        """Creando y clasificando data de Inferencia"""
        instancia_stl_raw = cache.get("tramites_stl")
        instancia_stl = json.loads(instancia_stl_raw) if instancia_stl_raw else {}

        InferenciaModel.ensure_indexes()
        inferencias_resultado_response = InferenciaModel.objects.all()

        def get_url_tramite(id_tramite):
            tramite = instancia_stl.get(str(id_tramite))
            if tramite:
                return (
                    tramite.get("url_tramite"),
                    tramite.get("url_redireccion"),
                    tramite.get("login"),
                )
            return None, None, None

        data_resultado_inferencia = []
        for inferencia in inferencias_resultado_response:
            if inferencia.estado != "ACT":
                continue

            rule = inferencia.rule.rule
            base_data = {
                "id": str(inferencia.id),
                "categoria": inferencia.categoria,
                "estado": inferencia.estado,
            }

            if inferencia.categoria == "tramite":
                url_tramite, url_redireccion, login = get_url_tramite(
                    inferencia.id_tramite
                )
                base_data.update(
                    {
                        "nombre_tramite": inferencia.nombre_tramite,
                        "dependencia_tramite": inferencia.dependencia_tramite,
                        "url_stl": config("URL_STL")
                        + config("FICHA_TRAMITE")
                        + str(inferencia.id_tramite),
                        "url_tramite": url_tramite,
                        "id_tramite": inferencia.id_tramite,
                        "url_redireccion": url_redireccion,
                        "login": login,
                    }
                )
            elif inferencia.categoria == "pasarela_pago":
                base_data.update(
                    {
                        "nombre_tramite": inferencia.nombre_tramite,
                        "dependencia_tramite": inferencia.dependencia_tramite,
                        "url_pasarela_pago": config("PASARELA_PAGO"),
                    }
                )
            elif inferencia.categoria == "mensaje_bienvenida":
                base_data.update(
                    {
                        "titulo": inferencia.titulo,
                        "descripcion": inferencia.descripcion,
                        "contactos": inferencia.contactos,
                        "correo_electronico": inferencia.correo_electronico,
                        "post_data": inferencia.post_data,
                    }
                )
            elif inferencia.categoria == "formulario":
                base_data.update(
                    {
                        "nombre_formulario": inferencia.nombre_formulario,
                        "grupo_formulario": DataSetResultadoInferencia.obtener_grupo_formulario(
                            inferencia.grupo_formulario
                        ),
                        "url_formulario": inferencia.url_formulario,
                    }
                )
            elif inferencia.categoria == "preguntas_frecuentes":
                base_data.update(
                    {
                        "titulo_pregunta": inferencia.titulo_pregunta,
                        "respuesta_pregunta": inferencia.respuesta_pregunta,
                    }
                )

            data_resultado_inferencia.append((rule, base_data))

        return data_resultado_inferencia

    @classmethod
    def data_changed(cls):
        """Evalúa si la data ha cambiado para cargarla nuevamente"""
        last_modification = (
            InferenciaModel.objects.order_by("-fecha_modificacion")
            .first()
            .fecha_modificacion
        )
        last_update = cache.get(cls._last_update_key)

        if last_update is None:
            cache.set(cls._last_update_key, last_modification, timeout=None)
            return False

        if isinstance(last_update, str):
            try:
                last_update = datetime.datetime.fromisoformat(last_update)
            except ValueError:
                last_update = None

        if not isinstance(last_update, datetime.datetime):
            last_update = None

        if last_update is None or last_modification > last_update:
            cache.set(cls._last_update_key, last_modification, timeout=None)
            return True

        return False

    @classmethod
    def refresh_dataset(cls):
        """Refresca la data de la cache de Inferencias"""
        instance = cls._create_inferencia_data()
        cls._update_cache(instance)
        return instance

    @classmethod
    def remove_inference_from_cache_by_id(cls, inferencia_id):
        """Remueve una inferencia de la caché"""
        inferencias = cls.get_instance()
        updated_inferencias = [
            tupla for tupla in inferencias if tupla[1]["id"] != inferencia_id
        ]
        cls._update_cache(updated_inferencias)
        return updated_inferencias

    # @classmethod
    # def update_cache_grupo_formulario(
    #     cls, nombre_grupo_antiguo, nombre_grupo_actualizado
    # ):
    #     """Actualiza la caché con el nuevo nombre del grupo de formulario"""
    #     instance = cls.get_instance()
    #     updated = False

    #     print("Nombre antiguo: ", nombre_grupo_antiguo)
    #     print("Nombre nuevo: ", nombre_grupo_actualizado)

    #     for idx, item in enumerate(instance):
    #         key, value = item

    #         grupo_formulario = value.get("grupo_formulario")

    #         if (
    #             grupo_formulario is not None
    #             and grupo_formulario == nombre_grupo_antiguo
    #         ):
    #             print("Valor antes de actualizar ", item)

    #             value["grupo_formulario"] = nombre_grupo_actualizado
    #             instance[idx] = (key, value)

    #             print("Valor después de actualizar: ", item)
    #             updated = True

    #     if updated:
    #         cls._update_cache(instance)
    #         print("La caché ha sido actualizada.")
    #     else:
    #         print("No se encontró el grupo de formulario en la caché")

    #     return instance

    @classmethod
    def _update_cache(cls, data):
        cache.delete(cls._instance_key)
        cache.set(cls._instance_key, data, timeout=None)
