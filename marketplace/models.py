from django.contrib.auth.models import User
from django.db import models
from collection.models import Pokemon


class marketPlacePokemon(models.Model):
    pokemon = models.ForeignObject(Pokemon)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Pokemon: " + self.pokemon.name + " Seller :" + self.seller.username + " Price: " + str(self.price)


class auctionHouse(models.Model):
    marketPlacePokemon = models.ForeignKey(marketPlacePokemon, on_delete=models.CASCADE)
