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
                rule=body.get("rule") or None,
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


class Keyword(APIView):
    def post(self, request, *args, **kwargs):
        body = request.data

        try:
            keywords = KeywordsModel(
                keyword=body.get("keyword"),
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

            # for keyword_record in keyword_records:
            #     keyword_record_dict = keyword_record.__dict__
            #     keyword_record_dict["_id"] = str(keyword_record_dict["_id"])
            #     keywords_data.append(keyword_record_dict)

        except Exception as e:
            return Response(
                {"message": f"Error en la creación de la nueva keyword {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    #     @api_view(['GET'])
    # def get_all_records(request):
    #     records = MyModel.objects.all()
    #     serializer = MyModelSerializer(records, many=True)
    #     return Response(serializer.data)


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
