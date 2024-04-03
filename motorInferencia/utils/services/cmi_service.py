"""
Archivo que contienene las soliciutedes para enviar y recibir información
de CMI, junto con la incorporación de WSO2
"""
import requests
from decouple import config
from django.core.cache import cache

from .wso2_service import WSO2Service


class CMIService:
    """
        Clase para realizar la consulta y posteo de información en el CMI
    """
    def crear_cabeceras(self):

        """
        Crea y retorna las cabeceras necesarias para realizar peticiones HTTP.

        Las cabeceras incluyen el tipo de contenido, el tipo de aceptación y la
        autorización utilizando un token de acceso obtenido desde un cache.

        Returns:
            dict[str, str]: Un diccionario con las cabeceras necesarias.
        """
        return {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cache.get('token_wso2')['access_token']}",
        }

    def manejar_respuesta(self, response):
        """
        Maneja la respuesta del servidor, obteniendo data y caso contrario, la data es rechazada,
        es un manejo de respuesta estánmdar para el servicio de CMI
        """
        if response.status_code == 200:
            response_data = response.json()
            print("Respuesta:", response_data)
        else:
            print("Error en la solicitud", response.status_code, response.text)

    def envio_data(self, data):
        """Envia data hacia el servicio del CMI"""
        url = config("URL_CMI") + "/enviar-datos?topic=" + config("TOPIC_BROKER")
        headers = self.crear_cabeceras()

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data, verify=False,
                timeout=config("TIMEOUT_CONNECTION")
            )
            self.manejar_respuesta(response)

            if response.status_code == 401:
                WSO2Service.refresh_token(cache.get("token_wso2")["refresh_token"])
                headers = self.crear_cabeceras()
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    verify=False,
                    timeout=config("TIMEOUT_CONNECTION")
                )
                self.manejar_respuesta(response)

        except requests.exceptions.RequestException as e:
            print("Error en la solicitud:", e)
