from django.contrib.auth.models import User
from django.db import models
from datetime import date

class Listing(models.Model):
    pokemon = models.ForeignKey("collection.Pokemon", on_delete=models.CASCADE, default=1) 
    price = models.PositiveBigIntegerField()
    date_posted = models.DateField(auto_now=True)
    status = models.CharField(max_length = 100)
    seller = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="seller_listing")
    buyer = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="buyer_listing")

    def post_Pokemon(pokemon, collection):
        if(Profile.contains(pokemon)):
            Collection.remove(pokemon)
            Listing.Pokemon.price == int(input('Price: '))
            Listing.date_posted = date.today()
            Listing.status = 'Not Sold'
            Listing.seller = User
            Listing.buyer = null

            Listing.append(pokemon)

    def post_Pokemon(Pokemon, Collection):
        if(Profile.contains(Pokemon)):
            Collection.remove(Pokemon)
            Listing.Pokemon.price == int(input('Price: '))
            Listing.date_posted = date.today()
            Listing.status = 'Not Sold'
            Listing.seller = User
            Listing.buyer = null

            Listing.append(Pokemon)
