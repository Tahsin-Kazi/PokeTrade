from django.contrib import admin
from .models import Pokemon 

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'name', 'owner',)
    search_fields = ('name', 'pokemon')
    list_filter = ('owner', 'date_collected')
    ordering = ('pokemon',)
    list_per_page = 30
