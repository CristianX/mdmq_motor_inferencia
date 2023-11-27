"""
Servicio de STL para obtener toda la data del servicio SOAP,
la data devuelta se lo poarsea con zeep ya que es un XML

"""
from decouple import config
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
    def consumo_tramite_soap(tramite_id):
        """
        Consume el servicio SOAP de STL para obtener información detallada de un trámite
        específico basado en su ID.

        Args:
            tramite_id (Any): El ID del trámite a consultar.

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

            tramite_consultado = tramites_por_id.get(tramite_id)

            url_formulario = tramite_consultado[
                "_x003C_UrlFormulario_x003E_k__BackingField"
            ]

            if url_formulario is not None:
                if url_formulario == "/MDMQ_Tramites/Solicitud?strestado=1":
                    return {
                        "url_tramite": config("URL_LOGIN") + str(tramite_id),
                        "url_redireccion": config("URL_STL") + url_formulario,
                        "login": True,
                    }
                elif "strestado=2" in url_formulario:
                    return {
                        "url_tramite": config("URL_LOGIN") + str(tramite_id),
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
        except (
            Exception
        ) as e:  # Esta es una captura general para otros errores imprevistos
            return Response(
                {"message": f"Error inesperado: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
