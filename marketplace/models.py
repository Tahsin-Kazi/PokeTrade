from django.contrib.auth.models import User
from django.db import models
from datetime import date

class Listing(models.Model):
    STATUS_OPTIONS = [
        ('not_sold', 'Not Sold'),
        ('sold', 'Sold'),
    ]
    pokemon = models.ForeignKey("collection.Pokemon", on_delete=models.CASCADE, default=1) 
    price = models.PositiveBigIntegerField()
    date_posted = models.DateField(auto_now=True)
    status = models.CharField(max_length = 10, choices=STATUS_OPTIONS, default='not_sold')
    seller = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="seller_listing")
    buyer = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="buyer_listing", null=True, blank=True)
    def __str__(self):
        return str(self.pokemon)

    def post_Pokemon(pokemon, collection, profile):
        if(profile.contains(pokemon)):
            sold_pokemon = collection.remove(pokemon)

            listing = Listing.objects.create(
                pokemon = sold_pokemon,
                price = int(input('Price: ')),
                date_posted = date.today(),
                status = 'Not Sold',
                seller = 'PokeTrade',
                buyer = None
            )
            listing.save()
            Listing.append(pokemon)

    
   
