from django.db import models


class ElectricityModel(models.Model):
    state = models.CharField(max_length=3, unique=False, null=False, blank=True)
    price = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
