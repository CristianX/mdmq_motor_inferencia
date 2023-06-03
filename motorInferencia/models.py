from django.db import models

# Create your models here.


class Keywords(models.Model):
    keyword = models.CharField(max_length=500)
    