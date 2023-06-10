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
)
from bson import ObjectId
from .utils.dataset_motor_inferencia import DataSetMotorInferencia

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
        except:
            return Response(
                "La consulta a enviar debe contener el campo 'mensaje'",
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
            print(rule)
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

            dependencias = [Dependencia(**dep) for dep in dependencias_data]
            instructivos = [Instructivo(**ins) for ins in instructivos_data]
            prerrequisitos = [Prerrequisito(**pre) for pre in prerrequisitos_data]

            inferencia = InferenciaModel(
                rule=RuleModel.objects.get(id=ObjectId(body.get("rule"))),
                dependencias=dependencias,
                instructivos=instructivos,
                prerrequisitos=prerrequisitos,
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
            )

            inferencia.save()

            print(inferencia)

            return Response(
                {"message": "Inferencia creada exitosamente"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"message": f"Error en la creación de la nueva inferencia {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
