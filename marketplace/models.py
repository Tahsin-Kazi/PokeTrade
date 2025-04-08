from django.contrib.auth.models import User
from django.db import models




class Listing(models.Model):
    pokemon = models.ForeignKey("collection.Pokemon", on_delete=models.CASCADE, default=1) 
    price = models.IntegerField(max_length = 500)
    date_posted = models.DateField(2025, 4, 6)
    status = models.CharField(max_length = 100)
    seller = models.ForeignKey("accounts.user", on_delete=models.CASCADE)
    buyer = models.ForeignKey("accounts.user", on_delete=models.CASCADE)




    
