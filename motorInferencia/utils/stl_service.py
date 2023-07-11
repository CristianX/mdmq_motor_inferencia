from rest_framework.response import Response
from zeep import Client

class STLService:
    def consumo_tramite_soap(id):
        try:
            client = Client(
                "http://172.22.0.104/MDMQ_Tramites_Servicios/General/TipoTramite.svc?wsdl"
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
        except:
            return Response(
                "Error en la conexión con STL. No se puede obtener url de tráramite"
            )
