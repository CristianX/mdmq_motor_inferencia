from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils.motor_inferencia import motor_inferencia
from motorInferencia.models import (
    RuleModel,
    KeywordsModel,
    InferenciaModel,
    Dependencia,
    Instructivo,
    Prerrequisito,
    DirigidoA,
    Horario,
    Contactos,
    BaseLegal,
    KeyWordsNoMappingModel,
)
from bson import ObjectId
from .utils.dataset_motor_inferencia import DataSetMotorInferencia
from .utils.data_resultado_inferencia import DataSetResultadoInferencia

# from django.forms.models import model_to_dict


class InferirConsulta(APIView):
    def post(self, request, *args, **kwargs):
        consulta = request.data

        try:
            response_motor_inferencia = motor_inferencia(consulta=consulta["mensaje"])
            return Response(
                {
                    "data": response_motor_inferencia,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                f"Error en realizar consulta {e}",
                status=status.HTTP_400_BAD_REQUEST,
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
            )
            rule.save()
            return Response(
                {"message": "Regla creada exitosamente"},
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
    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            dependencias_data = body.get("dependencias", [])
            instructivos_data = body.get("instructivos", [])
            prerrequisitos_data = body.get("prerrequisitos", [])
            dirigido_a_data = body.get("dirigido_a", [])
            horario_data = body.get("horario", {})
            contactos_data = body.get("contactos", [])
            base_legal_data = body.get("base_legal", [])

            dependencias = [Dependencia(**dep) for dep in dependencias_data]
            instructivos = [Instructivo(**ins) for ins in instructivos_data]
            prerrequisitos = [Prerrequisito(**pre) for pre in prerrequisitos_data]
            dirigido_a = [DirigidoA(**dirA) for dirA in dirigido_a_data]
            horario = Horario(**horario_data)
            contactos = [Contactos(**contact) for contact in contactos_data]
            base_legal = [BaseLegal(**baseLegal) for baseLegal in base_legal_data]

            inferencia = InferenciaModel(
                rule=RuleModel.objects.get(id=ObjectId(body.get("rule"))),
                descripcion=body.get("descripcion"),
                dependencias=dependencias,
                dirigido_a=dirigido_a,
                prerrequisitos=prerrequisitos,
                instructivos=instructivos,
                nota=body.get("nota"),
                costo_tramite=body.get("costo_tramite"),
                horario=horario,
                vigencia=body.get("vigencia"),
                contactos=contactos,
                base_legal=base_legal,
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
            )

            inferencia.save()

            DataSetResultadoInferencia.update_instance(
                (
                    inferencia.rule.rule,
                    {
                        "descripcion": inferencia.descripcion,
                        "dependencias": inferencia.dependencias,
                        "dirigido_a": inferencia.dirigido_a,
                        "prerrequisitos": inferencia.prerrequisitos,
                        "instructivos": inferencia.instructivos,
                        "nota": inferencia.nota,
                        "costo_tramite": inferencia.costo_tramite,
                        "horario": inferencia.horario,
                        "vigencia": inferencia.vigencia,
                        "contactos": inferencia.contactos,
                        "base_legal": inferencia.base_legal,
                    },
                )
            )

            return Response(
                {"message": "Inferencia creada exitosamente"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"message": f"Error en la creación de la nueva inferencia {e}"},
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
                {"mensaje": "Registro eliminado correctamente"},
                status=status.HTTP_202_ACCEPTED,
            )

        except:
            return Response(
                {"mensaje": "Error al eliminar el registro"},
                status=status.HTTP_400_BAD_REQUEST,
            )
