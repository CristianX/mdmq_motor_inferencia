from rest_framework.response import Response
from rest_framework import status
import requests
from decouple import config
from django.core.cache import cache
import base64


class WSO2Service:
    @staticmethod
    def generar_token():
        url = config("URL_WSO2") + "/oauth2/token"
        client_id = config("CLIENT_ID_WSO2")
        client_secret = config("CLIENT_SECRET_WSO2")
        username = config("USERNAME_WSO2")
        password = config("PASSWORD_WSO2")

        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )
        auth_token = f"Basic {encoded_credentials}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth_token,
        }

        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }

        try:
            response = requests.post(url, headers=headers, data=data, verify=False)

            if response.status_code == 200:
                response_data = response.json()
                cache.set("token_wso2", response_data, timeout=None)
            else:
                return Response(
                    {
                        "message": f"Error en la Solicitud: {response.status_code}, {response.text}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {"message": f"Error en la Solicitud: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def refresh_token(refresh_token):
        url = config("URL_WSO2") + "/oauth2/token"
        client_id = config("CLIENT_ID_WSO2")
        client_secret = config("CLIENT_SECRET_WSO2")

        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )
        auth_token = f"Basic {encoded_credentials}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth_token,
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": "default",
        }

        try:
            response = requests.post(url, headers=headers, data=data, verify=False)

            if response.status_code == 200:
                response_data = response.json()
                cache.set("token_wso2", response_data, timeout=None)
            else:
                return Response(
                    {
                        "message": f"Error en la Solicitud: {response.status_code}, {response.text}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {"message": f"Error en la Solicitud: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
