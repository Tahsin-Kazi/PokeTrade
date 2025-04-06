from django.contrib import admin
from .models import Pokemon 
from django.db.models.functions import Lower

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'name', 'owner', 'id')
    search_fields = ('name', 'pokemon')
    list_filter = ('owner', 'date_collected')
    ordering = (Lower('pokemon'),)
    list_per_page = 30

    fields = ('pokemon', 'name', 'owner', 'image', 'data')
    readonly_fields = ('data', 'image')
    
    def save_model (self, request, obj, form, change):
        
        if not obj.name:
            obj.name = obj.data.get('name')
        
        obj.save()
        super().save_model(request, obj, form, change)