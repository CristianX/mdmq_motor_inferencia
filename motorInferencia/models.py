from django.db import models

# Create your models here.


class KeyWors(models.Model):
    keywords = models.JSONField()

    # @classmethod
    # def create_keywords(cls, phrases, action):
    #     keywords = [(phrase, action) for phrase in phrases]
    #     return cls.objects.create(keywords=keywords)


# Crear una nueva instancia de KeyWors con las frases y la acción
# phrases = [
#     "Como puedo cambiar el nombre de un predio",
#     "Como registro un predio",
#     "registrar predio",
#     "compre un predio",
# ]
# action = "compra_predio"
# keywords = KeyWors.create_keywords(phrases, action)
