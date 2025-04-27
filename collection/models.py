from django.db import models
from pokebase import pokemon as fetch_pokemon  # Import the pokebase library
import os
from django.conf import settings
import random

class Pokemon(models.Model):
    name = models.CharField(max_length=100, blank=True)
    pokemon = models.CharField(max_length=100)
    owner = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, default=1, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    date_collected = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if not self.pk or not self.image:
            try:
                poke_data = fetch_pokemon(self.pokemon.lower())  # Fetch Pokemon by name
                
                varied_height = round(poke_data.height * .1 * random.uniform(0.9, 1.1), 2)
                varied_weight = round(poke_data.weight * .1 * random.uniform(0.9, 1.1), 2)
                
                abilities = [a.ability.name for a in poke_data.abilities]
                random_ability = random.choice(abilities) if abilities else None
                
                species_id = int(poke_data.species.url.split('/')[-2])
                
                excluded = ["ho-oh", "porygon-z", "jangmo-o", "hakomo-o", "kommo-o", "wo-chien", "chien-pao", "ting-lu", "chi-yu", "-mega", "-gmax", "-galar", "galarian", "-alola", "-paldea", "zygarde", "necrozma", "kyurem", "terapagos", "ogerpon", "gimmighoul", "palafin", "ursaluna", "calyrex", "zarude", "urshifu", "eternatus", "zacian", "zamazenta", "mimikyu", "silvally", "lycanroc", "minior", "oricorio", "wishiwashi", "toxtricity", "aegislash", "vivillon", "greninja", "tornadus", "thundurus", "landorus", "deoxys", "castform", "sawsbuck", "flabebe", "florges", "keldeo", "dialga", "palkia", "giratina", "darmanitan", "basculin", "shaymin", "rotom", "kyogre", "groudon", "unown", "pikachu"]
                
                if any(exclusion in poke_data.name for exclusion in excluded):
                    name = poke_data.name.title()
                    if "Gmax" in name:
                        name = name.replace("Gmax", "GMAX")
                else:
                    name = poke_data.name.title().replace('-', ' ')
                
                self.data = {
                    "id": species_id,
                    "name": name,
                    "height": varied_height,
                    "weight": varied_weight,
                    "types": [t.type.name.title() for t in poke_data.types],
                    "ability": random_ability.replace('-', ' ').title(),
                    "stats": {s.stat.name.replace('-',''): int(round(s.base_stat * random.uniform(0.8, 1.2), 0)) for s in poke_data.stats},
                }
                
                self.image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{poke_data.id}.png"
                
                if not self.name:
                    self.name = name
                
            except Exception as e:
                print(f"Error fetching data from PokeAPI: {e}")
                self.data = {"error": "Could not fetch data from PokeAPI"}

        super().save(*args, **kwargs)  # Call the parent class's save method

    class Meta:
        verbose_name_plural = "Pokemon"

    def __str__(self):
        return f"{self.owner.user.username}'s {self.name}"

class CollectedPokemon(models.Model):
    owner = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('listed', 'Listed for Sale'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.owner.user.username}'s {self.nickname or self.pokemon.name} ({self.status})"
