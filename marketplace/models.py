from django.contrib.auth.models import User
from django.db import models
from collection.models import Pokemon


class marketPlacePokemon(models.Model):
    pokemon = Pokemon.objects.get(id=1)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pokemon)

