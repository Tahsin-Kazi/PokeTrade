from django.contrib.auth.models import User
from django.db import models
from datetime import date
from collection.models import Pokemon

class Listing(models.Model):
    STATUS_OPTIONS = [
        ('not_sold', 'Not Sold'),
        ('sold', 'Sold'),
    ]
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=None) 
    price = models.PositiveBigIntegerField()
    date_posted = models.DateField(auto_now_add=True)
    status = models.CharField(max_length = 10, choices=STATUS_OPTIONS, default='not_sold')
    seller = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="seller_listing")
    buyer = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="buyer_listing", null=True, blank=True)
    def __str__(self):
        return str(self.pokemon)

    
   
