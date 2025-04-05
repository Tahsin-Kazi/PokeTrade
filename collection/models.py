from django.db import models
from pokebase import pokemon as fetch_pokemon  # Import the pokebase library
import os
from django.conf import settings

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    pokemon = models.CharField(max_length=100)
    owner = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, default=1)
    image = models.CharField(max_length=255, blank=True, null=True)
    date_collected = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)  

    def save(self, *args, **kwargs):
        if not self.pk or not self.image:
            try:
                poke_data = fetch_pokemon(self.pokemon.lower())  # Fetch Pokemon by name
                self.data = {
                    "id": poke_data.id,
                    "name": poke_data.name,
                    "height": poke_data.height,
                    "weight": poke_data.weight,
                    "types": [t.type.name for t in poke_data.types],
                    "abilities": [a.ability.name for a in poke_data.abilities],
                }
                # Set the image URL from the PokeAPI sprites
                pokedex_number = str(poke_data.id).zfill(4)  # Ensure the number is zero-padded (e.g., 001, 025)
                media_folder = os.path.join(settings.MEDIA_ROOT)  # Adjust folder name if needed
                for file in os.listdir(media_folder):
                    if file.startswith(f"poke_icon_{pokedex_number}"):
                        self.image = os.path.join(settings.MEDIA_URL, file)
                        break
                else:
                    # Default image if no match is found
                    self.image = os.path.join(settings.MEDIA_URL, 'poke_icon_0000_000_uk_n_00000000_f_n.png')
                
            except Exception as e:
                print(f"Error fetching data from PokeAPI: {e}")
                self.data = {"error": "Could not fetch data from PokeAPI"}

        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return f"{self.owner.user.username}'s {self.name}"