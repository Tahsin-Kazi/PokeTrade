from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    poke_name = models.CharField(max_length=100)
    image = models.URLField()
    data = models.JSONField(default=dict)

    def __str__(self):
        return "Name: " + self.name + "\nPokemon: " + self.poke_name