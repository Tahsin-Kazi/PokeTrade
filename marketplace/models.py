from django.contrib.auth.models import User
from django.db import models
from collection.models import Pokemon


class Listing(models.Model):
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)