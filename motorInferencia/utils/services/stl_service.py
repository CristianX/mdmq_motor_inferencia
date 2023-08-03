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
                return f"https://pam.quito.gob.ec/PAM/PopupLogin.aspx?tipoProceso={id}"
            elif resultado["_x003C_UrlFormulario_x003E_k__BackingField"] == "":
                return None
            else:
                return resultado["_x003C_UrlFormulario_x003E_k__BackingField"]
        except Exception as e:
            return Response(
                {"message": f"Error en la conexión con WS STL: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
