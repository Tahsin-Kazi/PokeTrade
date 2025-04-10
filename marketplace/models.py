from django.contrib.auth.models import User
from django.db import models

class Listing(models.Model):
    pokemon = models.ForeignKey("collection.Pokemon", on_delete=models.CASCADE, default=1) 
    price = models.IntegerField()
    date_posted = models.DateField(auto_now=True)
    status = models.CharField(max_length = 100)
    seller = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="seller")
    buyer = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="buyer")




    
