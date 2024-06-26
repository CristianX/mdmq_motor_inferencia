import json
from datetime import datetime, timezone

from bson import ObjectId
from decouple import config
from django.core.cache import cache
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from motorInferencia.models import (
    CatalogoGrupoFormularioModel,
    InferenciaModel,
    KeywordsModel,
    KeyWordsNoMappingModel,
    RuleModel,
)
from motorInferencia.serializers import (
    CatalogoGrupoFormularioSerializer,
    InferenciaSerializer,
)

from .utils.data_resultado_inferencia import DataSetResultadoInferencia
from .utils.dataset_motor_inferencia import DataSetMotorInferencia
from .utils.motor_inferencia import motor_inferencia
from .utils.services.cmi_service import CMIService
from .utils.services.stl_service import STLService

# from django.forms.models import model_to_dict

# pylint: disable=no-member

cmi_service = CMIService()


class InferirConsulta(APIView):
    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            response_motor_inferencia = motor_inferencia(consulta=body.get("mensaje"))
            # Enviando datos a CMI
            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "consulta": body.get("mensaje"),
            #     }
            # )
            return Response(
                {
                    "data": response_motor_inferencia,
                },
                status=status.HTTP_200_OK,
            )
        except Http404 as e:
            return Response(
                {
                    "error": str(e),
                    "url": "https://pam.quito.gob.ec/PAM/Inicio.aspx",
                    "contactos": "3952300",
                    "ext": "20127",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                f"Error al realizar la consulta {e}", status=status.HTTP_400_BAD_REQUEST
            )


class Rule(APIView):
    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            rule = RuleModel(
                rule=body.get("rule").lower() or None,
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
                estado=body.get("estado"),
            )

            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "tipo_peticion": "POST",
            #         "coleccion": "Reglas",
            #         "regla": body.get("rule").lower() or None,
            #         "usuario_creacion": body.get("usuario_creacion"),
            #         "dispositivo_creacion": body.get("dispositivo_creacion"),
            #         "usuario_modificacion": body.get("usuario_modificacion"),
            #         "dispositivo_modificacion": body.get("dispositivo_modificacion"),
            #         "estado": body.get("estado"),
            #     }
            # )

            rule.save()

            return Response(
                {
                    "message": "Regla creada exitosamente",
                    "regla_id": str(rule.id),
                    "regla": rule.rule,
                    "estado_regla": rule.estado,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"message": f"Error en la creación de la nueva regla {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            try:
                rule = RuleModel.objects(id=ObjectId(kwargs.get("id"))).first()
                if not rule:
                    return Response(
                        {"message": "No se ha encontrado la regla indicada"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                return Response({"id": str(rule.id), "rule": rule.rule})
            except:
                return Response(
                    {"message": "Error al obtener la regla"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            try:
                rules = RuleModel.objects()
                data = [{"id": str(rl.id), "rule": rl.rule} for rl in rules]
                return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {f"Error al obtener las reglas: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def put(self, request, *args, **kwargs):
        rule = None
        try:
            rule = RuleModel.objects(id=ObjectId(kwargs.get("id"))).first()

            if not rule:
                return Response(
                    {"message": "Regla no encontrada"}, status=status.HTTP_404_NOT_FOUND
                )

            body = request.data

            if body.get("rule"):
                existing_rule = RuleModel.objects(rule=body.get("rule").lower()).first()
                if existing_rule and (existing_rule.id != rule.id):
                    return Response(
                        {"message": "Esa regla ya se encuentra registrada"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                rule.rule = body.get("rule").lower()

            rule.usuario_modificacion = body.get("usuario_modificacion")
            rule.dispositivo_modificacion = body.get("dispositivo_modificacion")

            # Alimentación CMI
            rule_to_dict = rule.to_mongo().to_dict()

            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "tipo_peticion": "PUT",
            #         "coleccion": "Reglas",
            #         "id": str(rule_to_dict.get("id")),
            #         "regla": rule_to_dict.get("rule"),
            #         "fecha_creacion": str(rule_to_dict.get("fecha_creacion")),
            #         "usuario_creacion": rule_to_dict.get("usuario_creacion", None),
            #         "dispositivo_creacion": rule_to_dict.get(
            #             "dispositivo_creacion", None
            #         ),
            #         "fecha_modificacion": str(rule_to_dict.get("fecha_modificacion")),
            #         "usuario_modificacion": rule_to_dict.get(
            #             "usuario_modificacion", None
            #         ),
            #         "dispositivo_modificacion": rule_to_dict.get(
            #             "dispositivo_modificacion", None
            #         ),
            #         "estado": rule_to_dict.get("estado", None),
            #     }
            # )

            rule.save()

            return Response(
                {"message": "Regla modificada correctamente"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Error al actualizar la regla: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        rule = None
        try:
            rule = RuleModel.objects(id=ObjectId(kwargs.get("id"))).first()
            if not rule:
                return Response(
                    {"message": "Regla no encontrada"}, status=status.HTTP_404_NOT_FOUND
                )

            rule_to_dict = rule.to_mongo().to_dict()

            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "tipo_peticion": "DELETE",
            #         "coleccion": "Reglas",
            #         "id": str(rule_to_dict.get("id")),
            #         "regla": rule_to_dict.get("rule"),
            #         "fecha_creacion": str(rule_to_dict.get("fecha_creacion")),
            #         "usuario_creacion": rule_to_dict.get("usuario_creacion", None),
            #         "dispositivo_creacion": rule_to_dict.get(
            #             "dispositivo_creacion", None
            #         ),
            #         "fecha_modificacion": str(rule_to_dict.get("fecha_modificacion")),
            #         "usuario_modificacion": rule_to_dict.get(
            #             "usuario_modificacion", None
            #         ),
            #         "dispositivo_modificacion": rule_to_dict.get(
            #             "dispositivo_modificacion", None
            #         ),
            #         "estado": rule_to_dict.get("estado", None),
            #     }
            # )

            rule.delete()

            DataSetMotorInferencia.refresh_dataset()
            DataSetResultadoInferencia.refresh_dataset()

            return Response(
                {"message": "Regla eliminada"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"message": f"Error al eliminar la regla: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Keyword(APIView):
    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            keywords = KeywordsModel(
                keyword=body.get("keyword").lower(),
                rule=RuleModel.objects.get(id=ObjectId(body.get("rule"))),
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
            )

            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "tipo_peticion": "POST",
            #         "coleccion": "Frases",
            #         "keyword": body.get("keyword").lower(),
            #         "regla_id": str(
            #             RuleModel.objects.get(id=ObjectId(body.get("rule")))["id"]
            #         ),
            #         "regla": RuleModel.objects.get(id=ObjectId(body.get("rule")))[
            #             "rule"
            #         ],
            #         "usuario_creacion": body.get("usuario_creacion"),
            #         "dispositivo_creacion": body.get("dispositivo_creacion"),
            #         "usuario_modificacion": body.get("usuario_modificacion"),
            #         "dispositivo_modificacion": body.get("dispositivo_modificacion"),
            #     }
            # )

            keywords.save()

            DataSetMotorInferencia.update_instance(
                (keywords.keyword, keywords.rule.rule)
            )

            return Response(
                {"message": "Keyword creada exitosamente"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"message": f"Error en la creación de la nueva keyword {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            try:
                keyword = KeywordsModel.objects(id=ObjectId(kwargs.get("id"))).first()
                if not keyword:
                    return Response(
                        {"message": "Keyword no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                return Response(
                    {
                        "id": str(keyword.id),
                        "keyword": keyword.keyword,
                        "rule": keyword.rule.rule,
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"message": f"Error al obtener la keyword {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            try:
                keywords = KeywordsModel.objects()
                data = [
                    {"id": str(kw.id), "keyword": kw.keyword, "rule": kw.rule.rule}
                    for kw in keywords
                ]
                return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": f"Error al obtener las keywords {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def put(self, request, *args, **kwargs):
        keyword = None
        try:
            keyword = KeywordsModel.objects(id=ObjectId(kwargs.get("id"))).first()

            if not keyword:
                return Response(
                    {"message": "Keyword no encontrada"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            body = request.data

            if body.get("keyword"):
                existing_keyword = KeywordsModel.objects(
                    keyword=body.get("keyword").lower()
                ).first()
                # print(keyword.id)
                if existing_keyword and (existing_keyword.id != keyword.id):
                    return Response(
                        {"message": "Esa frase ya se encuentra asignada a una regla"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                keyword.keyword = body.get("keyword").lower()

            if body.get("rule"):
                rule = RuleModel.objects(id=ObjectId(body.get("rule"))).first()
                if not rule:
                    return (
                        Response(
                            {"message": "Regla no encontrada"},
                            status=status.HTTP_404_NOT_FOUND,
                        ),
                    )
                keyword.rule = rule

            keyword.usuario_modificacion = body.get("usuario_modificacion")
            keyword.dispositivo_modificacion = body.get("dispositivo_modificacion")

            keyword_to_dict = keyword.to_mongo().to_dict()

            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "tipo_peticion": "PUT",
            #         "coleccion": "Frases",
            #         "id": str(keyword_to_dict.get("id")),
            #         "frase": keyword_to_dict.get("keyword"),
            #         "regla": str(keyword_to_dict.get("rule")),
            #         "fecha_creacion": str(keyword_to_dict.get("fecha_creacion")),
            #         "usuario_creacion": keyword_to_dict.get("usuario_creacion", None),
            #         "dispositivo_creacion": keyword_to_dict.get(
            #             "dispositivo_creacion", None
            #         ),
            #         "fecha_modificacion": str(
            #             keyword_to_dict.get("fecha_modificacion")
            #         ),
            #         "usuario_modificacion": keyword_to_dict(
            #             "usuario_modificacion", None
            #         ),
            #         "dispositivo_modificacion": keyword_to_dict(
            #             "dispositivo_modificacion", None
            #         ),
            #     }
            # )

            keyword.save()

            DataSetMotorInferencia.refresh_dataset()

            return Response(
                {"message": "Keyword actualizada exitosamente"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": f"Error al actualizar la keyword: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        keyword = None
        try:
            keyword = KeywordsModel.objects(id=ObjectId(kwargs.get("id"))).first()
            if not keyword:
                return Response(
                    {"message": "Frase no encontrada"}, status=status.HTTP_404_NOT_FOUND
                )

            keyword_to_dict = keyword.to_mongo().to_dict()

            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "tipo_peticion": "DELETE",
            #         "coleccion": "Frases",
            #         "id": str(keyword_to_dict.get("id")),
            #         "frase": keyword_to_dict.get("keyword"),
            #         "regla": str(keyword_to_dict.get("rule")),
            #         "fecha_creacion": str(keyword_to_dict.get("fecha_creacion")),
            #         "usuario_creacion": keyword_to_dict.get("usuario_creacion", None),
            #         "dispositivo_creacion": keyword_to_dict.get(
            #             "dispositivo_creacion", None
            #         ),
            #         "fecha_modificacion": str(
            #             keyword_to_dict.get("fecha_modificacion")
            #         ),
            #         "usuario_modificacion": keyword_to_dict(
            #             "usuario_modificacion", None
            #         ),
            #         "dispositivo_modificacion": keyword_to_dict(
            #             "dispositivo_modificacion", None
            #         ),
            #     }
            # )

            keyword.delete()

            DataSetMotorInferencia.refresh_dataset()

            return Response(
                {"message": "Frase eliminada"}, status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response(
                {"message": f"Error al eliminar la frase {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Inferencia(APIView):
    def get(self, request, *args, **kwargs):
        instancia_stl = json.loads(cache.get("tramites_stl"))
        excluded_fields = [
            "usuario_creacion",
            "fecha_creacion",
            "dispositivo_creacion",
            "usuario_modificacion",
            "dispositivo_modificacion",
            "fecha_modificacion",
        ]

        if "id" in kwargs:
            try:
                inferencia = InferenciaModel.objects(
                    id=ObjectId(kwargs.get("id"))
                ).first()
                if not inferencia:
                    return Response(
                        {"message": "Inferencia no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                inf_dict = inferencia.to_mongo().to_dict()
                inf_dict = {
                    k: str(v) if isinstance(v, ObjectId) else v
                    for k, v in inf_dict.items()
                    if k not in excluded_fields
                }

                if inf_dict["categoria"] == "informacion":
                    inf_dict["url_stl"] = config("URL_STL") + str(
                        inf_dict["id_tramite"]
                    )
                    inf_dict["url_tramite"] = (
                        instancia_stl.get(str(inf_dict["id_tramite"])).get(
                            "url_tramite"
                        )
                        if instancia_stl.get(str(inf_dict["id_tramite"]))
                        else None
                    )
                    inf_dict["url_redireccion"] = (
                        instancia_stl.get(str(inf_dict["id_tramite"])).get(
                            "url_redireccion"
                        )
                        if instancia_stl.get(str(inf_dict["id_tramite"]))
                        else None
                    )
                    inf_dict["login"] = (
                        instancia_stl.get(str(inf_dict["id_tramite"])).get("login")
                        if instancia_stl.get(str(inf_dict["id_tramite"]))
                        else None
                    )
                elif inf_dict["categoria"] == "pasarela_pago":
                    inf_dict["url_pasarela_pago"] = config("PASARELA_PAGO")

                return Response(inf_dict, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"message": f"Error al obtener la inferencia: {e}"})

        else:
            try:
                inferencias = InferenciaModel.objects()
                inferencias_list = []

                for inf in inferencias:
                    inf_dict = inf.to_mongo().to_dict()

                    inf_dict = {
                        k: str(v) if isinstance(v, ObjectId) else v
                        for k, v in inf_dict.items()
                        if k not in excluded_fields
                    }

                    if inf_dict["categoria"] == "informacion":
                        inf_dict["url_stl"] = config("URL_STL") + str(
                            inf_dict["id_tramite"]
                        )
                        inf_dict["url_tramite"] = (
                            instancia_stl.get(str(inf_dict["id_tramite"])).get(
                                "url_tramite"
                            )
                            if instancia_stl.get(str(inf_dict["id_tramite"]))
                            else None
                        )
                        inf_dict["url_redireccion"] = (
                            instancia_stl.get(str(inf_dict["id_tramite"])).get(
                                "url_redireccion"
                            )
                            if instancia_stl.get(str(inf_dict["id_tramite"]))
                            else None
                        )
                        inf_dict["login"] = (
                            instancia_stl.get(str(inf_dict["id_tramite"])).get("login")
                            if instancia_stl.get(str(inf_dict["id_tramite"]))
                            else None
                        )
                        inferencias_list.append(inf_dict)
                    elif inf_dict["categoria"] == "pasarela_pago":
                        inf_dict["url_pasarela_pago"] = config("PASARELA_PAGO")
                        inferencias_list.append(inf_dict)

                    else:
                        inferencias_list.append(inf_dict)

                return Response(
                    inferencias_list,
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {"message": f"Error al obtener las inferencias: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            rule_id = body.get("rule")
            if rule_id:
                body["rule"] = RuleModel.objects.get(id=ObjectId(rule_id))
            inferencia = InferenciaModel(**body)

            # Envio de datos a CMI
            inferencia_dict = inferencia.to_mongo().to_dict()

            # cmi_service.envio_data(
            #     {
            #         "SISTEMA": "MOTOR_INFERENCIA",
            #         "tipo_peticion": "POST",
            #         "coleccion": "Inferencias",
            #         "regla": str(inferencia_dict.get("rule")),
            #         "estado": inferencia_dict.get("estado", None),
            #         "categoria": inferencia_dict.get("categoria", None),
            #         "fecha_creacion": str(inferencia_dict.get("fecha_creacion")),
            #         "usuario_creacion": inferencia_dict.get("usuario_creacion"),
            #         "dispositivo_creacion": inferencia_dict.get("dispositivo_creacion"),
            #         "fecha_modificacion": str(
            #             inferencia_dict.get("fecha_modificacion")
            #         ),
            #         "nombre_tramite": inferencia_dict.get("nombre_tramite"),
            #         "dependencia_tramite": inferencia_dict.get("dependencia_tramite"),
            #         "url_stl": inferencia_dict.get("url_stl", None),
            #     }
            # )

            inferencia.save()
            return Response(
                {"message": "Inferencia Creada Correctamente"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                f"Error al cargar datos {e}", status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return Response(
                {"message": "ID de la inferencia no proporcionado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            inferencia = InferenciaModel.objects.get(id=ObjectId(kwargs.get("id")))
        except InferenciaModel.DoesNotExist:
            return Response(
                {"message": "Inferencia no encontrada"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        data["fecha_modificacion"] = datetime.now(timezone.utc)

        # Actualiza todos los campos dinámicamente
        for key, value in data.items():
            if key in inferencia._fields:
                setattr(inferencia, key, value)
            else:
                inferencia[key] = value

        inferencia.save()

        return Response(
            {"message": "Inferencia actualizada correctamente"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        if "id" in kwargs:
            try:
                inferencia = InferenciaModel.objects(
                    id=ObjectId(kwargs.get("id"))
                ).first()

                if not inferencia:
                    return Response(
                        {"message": "Inferencia no encontrada"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                inferencia.estado = "INA"

                # Desactivando frases
                # keywords_associated = KeywordsModel.objects(rule=inferencia.rule)
                # for keyword in keywords_associated:
                #     keyword.estadp = "INA"
                #     keyword.save()

                # Desactivando reglas
                inferencia.rule.estado = "INA"

                inferencia_dict = inferencia.to_mongo().to_dict()

                # cmi_service.envio_data(
                #     {
                #         "SISTEMA": "MOTOR_INFERENCIA",
                #         "tipo_peticion": "DELETE",
                #         "coleccion": "Inferencias",
                #         "regla": str(inferencia_dict.get("rule")),
                #         "estado": inferencia_dict.get("estado", None),
                #         "categoria": inferencia_dict.get("categoria", None),
                #         "fecha_creacion": str(inferencia_dict.get("fecha_creacion")),
                #         "usuario_creacion": inferencia_dict.get("usuario_creacion"),
                #         "dispositivo_creacion": inferencia_dict.get(
                #             "dispositivo_creacion"
                #         ),
                #         "fecha_modificacion": str(
                #             inferencia_dict.get("fecha_modificacion")
                #         ),
                #         "nombre_tramite": inferencia_dict.get("nombre_tramite"),
                #         "dependencia_tramite": inferencia_dict.get(
                #             "dependencia_tramite"
                #         ),
                #         "url_stl": inferencia_dict.get("url_stl", None),
                #     }
                # )

                DataSetResultadoInferencia.remove_inference_from_cache_by_id(
                    kwargs.get("id")
                )
                inferencia.rule.save()
                inferencia.save()

                return Response(
                    {"message": "La inferencia ha sido dada de baja exitosamente."},
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {"message": f"Error en dar de baja la Inferencia: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {"message": "Id de la Inferencia no proporcionado"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class KeywordNoMapping(APIView):
    def delete(self, request, keyword_no_mapping_id):
        try:
            keyword_no_mapping = KeyWordsNoMappingModel.objects.get(
                id=keyword_no_mapping_id
            )
            keyword_no_mapping.delete()
            return Response(
                {"message": "Registro eliminado correctamente"},
                status=status.HTTP_202_ACCEPTED,
            )

        except:
            return Response(
                {"message": "Error al eliminar el registro"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, *args, **kwargs):
        try:
            keywords_no_mapping = KeyWordsNoMappingModel.objects().order_by(
                "-conteo_consulta"
            )
            data = [
                {
                    "id": str(kw.id),
                    "keyword": kw.keyword,
                    "conteo_consulta": kw.conteo_consulta,
                }
                for kw in keywords_no_mapping
            ]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"Error al obtener las keywords {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class KeywordsByRule(APIView):
    def get(self, request, rule_id, *args, **kwargs):
        try:
            keywords = KeywordsModel.objects(rule=ObjectId(rule_id))
            if not keywords:
                return Response(
                    {
                        "message": "No se encontraron registros para la regla especificada."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = [
                {"id": str(kw.id), "keyword": kw.keyword, "rule": kw.rule.rule}
                for kw in keywords
            ]
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": f"Error al obtener frases para esa regla {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Tuplas(APIView):
    def get(self, request, *args, **kwargs):
        if DataSetResultadoInferencia.get_instance():
            return Response(
                {"found": True, "resultado": DataSetResultadoInferencia.get_instance()},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Inferencias no existentes"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GrupoFormularios(APIView):
    def post(self, request):
        serializer = CatalogoGrupoFormularioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Grupo de formulario creado exitosamente"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            try:
                grupo_formulario = CatalogoGrupoFormularioModel.objects.get(
                    id=ObjectId(kwargs.get("id"))
                )
                serializer = CatalogoGrupoFormularioSerializer(grupo_formulario)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except CatalogoGrupoFormularioModel.DoesNotExist:
                return Response(
                    {"message": "Grupo de Formularios no encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                return Response(
                    {"message": f"Error al obtener el Grupo de Formularios: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            try:
                grupo_formularios = CatalogoGrupoFormularioModel.objects.all()
                serializer = CatalogoGrupoFormularioSerializer(
                    grupo_formularios, many=True
                )
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"message": f"Error al obtener los Grupos de Formularios: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def put(self, request, *args, **kwargs):
        # nombre_grupo_nuevo = request.data.get("nombre_grupo")
        if "id" not in kwargs:
            return Response(
                {"message": "Falta el ID del Grupo de Formularios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            grupo_formulario = CatalogoGrupoFormularioModel.objects.get(
                id=ObjectId(kwargs.get("id"))
            )

            # nombre_grupo_antiguo = grupo_formulario.nombre_grupo

            serializer = CatalogoGrupoFormularioSerializer(
                grupo_formulario, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                # Actualizar la caché
                # nombre_grupo_actualizado = (
                #     DataSetResultadoInferencia.obtener_grupo_formulario(
                #         grupo_formulario.id
                #     )
                # )

                # if nombre_grupo_actualizado:
                #     print(
                #         f"Actualizando caché con nombre de grupo: {nombre_grupo_actualizado}"
                #     )
                #     DataSetResultadoInferencia.update_cache_grupo_formulario(
                #         nombre_grupo_antiguo, nombre_grupo_actualizado
                #     )
                # else:
                #     print("No se proporcionó un nombre de grupo actualizado")

                # Actualizar la fecha de modificación de los registros relacionados en InferenciaModel
                inferencias = InferenciaModel.objects(
                    grupo_formulario=ObjectId(kwargs.get("id"))
                )

                print("Inferencias encontradas: ", inferencias)

                for inferencia in inferencias:
                    inferencia.fecha_modificacion = datetime.now(timezone.utc)
                    inferencia.save()

                return Response(
                    {"message": "Grupo de Formularios actualizado exitosamente"},
                    status=status.HTTP_200_OK,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CatalogoGrupoFormularioModel.DoesNotExist:
            return Response(
                {"message": "Grupo de Formularios no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"Error: {e}")
            return Response(
                {"message": f"Error al actualizar el Grupo de Formularios: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
