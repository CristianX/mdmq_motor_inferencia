import json

from decouple import config
from django.core.cache import cache
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.response import Response
from zeep import Client
from zeep.exceptions import Fault, TransportError


class STLService:
    """
    Clase de STLService para consumo de servicio SOAP
    """

    @staticmethod
    def consumo_tramite_soap():
        """
        Consume el servicio SOAP de STL para obtener información detallada de un trámite
        específico basado en su ID.


        Returns:
            dict | Response: Un diccionario con los detalles del trámite o una respuesta de error.
        """

        try:
            client = Client(
                config("URL_STL_TIPO_TRAMITE")
                + "/MDMQ_Tramites_Servicios/General/TipoTramite.svc?wsdl"
            )
            resultado = client.service.ConsultarTodosParaSolicitud()

            tramites_por_id = {
                t["_x003C_TipoTramiteId_x003E_k__BackingField"]: t for t in resultado
            }

            tramites_clasificados = {}
            for tr_id, tramite in tramites_por_id.items():
                clasificado = STLService.clasificar_tramite(tramite)
                tramites_clasificados[tr_id] = clasificado

            cache.set("tramites_stl", json.dumps(tramites_clasificados), timeout=None)

            # return tramites_clasificados

        except Fault as fault:
            return Response(
                {
                    "message": f"Error SOAP Fault: Code={fault.code}, Reason={fault.detail}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TransportError as transport_error:
            return Response(
                {"message": f"Error de transporte SOAP: {transport_error}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except RequestException as request_exception:
            return Response(
                {"message": f"Error en la solicitud HTTP: {request_exception}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": f"Error inesperado: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def clasificar_tramite(tramite):
        """
        Clasifica un trámite según condiciones específicas.

        Args:
            tramite (dict): Los detalles del trámite.

        Returns:
            dict: Un diccionario con los detalles clasificados del trámite.
        """
        url_formulario = tramite["_x003C_UrlFormulario_x003E_k__BackingField"]

        if url_formulario is not None:
            if url_formulario == "/MDMQ_Tramites/Solicitud?strestado=1":
                return {
                    "url_tramite": config("URL_LOGIN")
                    + str(tramite["_x003C_TipoTramiteId_x003E_k__BackingField"]),
                    "url_redireccion": config("URL_STL") + url_formulario,
                    "login": True,
                }
            elif "strestado=2" in url_formulario:
                return {
                    "url_tramite": config("URL_LOGIN")
                    + str(tramite["_x003C_TipoTramiteId_x003E_k__BackingField"]),
                    "url_redireccion": url_formulario + "&token=",
                    "login": True,
                }
            else:
                return {
                    "url_tramite": url_formulario,
                    "url_redireccion": url_formulario,
                    "login": False,
                }
        else:
            return {
                "url_tramite": None,
                "url_redireccion": None,
                "login": False,
            }
