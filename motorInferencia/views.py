from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils.motor_inferencia import motor_inferencia
from motorInferencia.models import RuleModel, KeywordsModel
from bson import ObjectId
from .utils.dataset_motor_inferencia import set_keywords
from django.conf import settings

# from django.forms.models import model_to_dict


class InferirConsulta(APIView):
    def post(self, request, *args, **kwargs):
        consulta = request.data
        # all_keywords = KeywordsModel.objects.all()
        # print(all_keywords)

        try:
            response_motor_inferencia = motor_inferencia(consulta=consulta["mensaje"])
            print(settings.DATA_KEYWORDS)
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
            rule = RuleModel.objects.create(
                rule=body.get("rule") or None,
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
            )
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
            keywordsResponse = KeywordsModel.objects.create(
                keyword=body.get("keyword"),
                rule=RuleModel.objects.get(_id=ObjectId(body.get("rule"))),
                usuario_creacion=body.get("usuario_creacion"),
                dispositivo_creacion=body.get("dispositivo_creacion"),
                usuario_modificacion=body.get("usuario_modificacion"),
                dispositivo_modificacion=body.get("dispositivo_modificacion"),
            )

            set_keywords((keywordsResponse.keyword, keywordsResponse.rule.rule))
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
