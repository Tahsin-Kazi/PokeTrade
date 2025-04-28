from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('get_pokemon_name', 'seller', 'price',)
    search_fields = ('title', 'description')
    list_filter = ()
    ordering = ()
    list_per_page = 30
    
    def get_pokemon_name(self, obj):
        return obj.pokemon.name if obj.pokemon else None
    get_pokemon_name.short_description = "Pokemon"