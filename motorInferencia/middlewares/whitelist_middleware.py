from django.http import HttpResponseForbidden
from decouple import config


class WhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Aquí se define la lista blanca de IPs
        self.whitelist = [config("WHITELIST_CONSUMO")]

    def __call__(self, request):
        # Obtienes la dirección IP del request
        ip = request.META.get("REMOTE_ADDR")

        # Si la dirección IP no está en la lista blanca, devuelve un error 403
        if ip not in self.whitelist:
            return HttpResponseForbidden("Forbidden")

        # Si está en la lista blanca, simplemente pasa la solicitud al siguiente middleware
        response = self.get_response(request)
        return response
