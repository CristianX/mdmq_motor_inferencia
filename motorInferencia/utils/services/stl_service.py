from rest_framework.response import Response
from zeep import Client
from decouple import config
from rest_framework import status


class STLService:
    def consumo_tramite_soap(id):
        try:
            client = Client(
                config("URL_STL_TIPO_TRAMITE")
                + "/MDMQ_Tramites_Servicios/General/TipoTramite.svc?wsdl"
            )
            resultado = client.service.ConsultarPorId(idTipoTramite=id)

            if (
                resultado["_x003C_UrlFormulario_x003E_k__BackingField"]
                == "/MDMQ_Tramites/Solicitud?strestado=1"
            ):
                return {
                    "url_tramite": config("URL_LOGIN") + str(id),
                    "url_redireccion": config("URL_STL")
                    + resultado["_x003C_UrlFormulario_x003E_k__BackingField"],
                    "login": True,
                }
            elif "strestado=2" in str(
                resultado["_x003C_UrlFormulario_x003E_k__BackingField"]
            ):
                return {
                    "url_tramite": config("URL_LOGIN") + str(id),
                    "url_redireccion": resultado[
                        "_x003C_UrlFormulario_x003E_k__BackingField"
                    ]
                    + "&token=",
                    "login": True,
                }
            elif resultado["_x003C_UrlFormulario_x003E_k__BackingField"] == "":
                return {"url_tramite": None, "url_redireccion": None, "login": False}
            else:
                return {
                    "url_tramite": resultado[
                        "_x003C_UrlFormulario_x003E_k__BackingField"
                    ],
                    "url_redireccion": resultado[
                        "_x003C_UrlFormulario_x003E_k__BackingField"
                    ],
                    "login": False,
                }
        except Exception as e:
            return Response(
                {"message": f"Error en la conexión con WS STL: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
