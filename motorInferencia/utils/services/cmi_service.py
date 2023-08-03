from rest_framework.response import Response
from rest_framework import status
import requests
from decouple import config
from django.core.cache import cache
from .wso2_service import WSO2Service


class CMIService:
    def crear_cabeceras(self):
        return {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cache.get('token_wso2')['access_token']}",
        }

    def manejar_respuesta(self, response):
        if response.status_code == 200:
            response_data = response.json()
            print("Respuesta:", response_data)
        else:
            print("Error en la solicitud", response.status_code, response.text)

    def envio_data(self, data):
        url = config("URL_CMI") + "/enviar-datos?topic=" + config("TOPIC_BROKER")
        headers = self.crear_cabeceras()

        try:
            response = requests.post(url, headers=headers, json=data, verify=False)
            self.manejar_respuesta(response)

            if response.status_code == 401:
                WSO2Service.refresh_token(cache.get("token_wso2")["refresh_token"])
                headers = self.crear_cabeceras()
                response = requests.post(url, headers=headers, json=data, verify=False)
                self.manejar_respuesta(response)

        except requests.exceptions.RequestException as e:
            print("Error en la solicitud:", e)
