# app/management/commands/add_pokemon.py
from django.core.management.base import BaseCommand
from app.utils import add_to_marketplace  # Import your function

class Command(BaseCommand):
    help = 'Add random Pokémon to the marketplace'

    def handle(self, *args, **kwargs):
        add_to_marketplace()  # Call your method to add Pokémon
        self.stdout.write(self.style.SUCCESS('Successfully added Pokémon to marketplace'))
