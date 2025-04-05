from django.contrib import admin
from .models import Profile 
from django.utils.html import format_html

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_collection', 'get_friends')
    search_fields = ('user__username',)
    ordering = ('user',)
    list_per_page = 30
    list_select_related = ('user',)
    
    def get_collection(self, obj):
        collection = obj.pokemon_set.all()
        if not collection:
            return "No Pokemon"
        return format_html("<br>".join([f"{p.pokemon} ({p.name})" for p in collection]))
    get_collection.short_description = "Collection"
    
    def get_friends(self, obj):
        friends = obj.friends.all()
        if not friends:
            return "No Friends"
        return format_html("<br>".join([f"{friend.username}" for friend in friends]))
    get_friends.short_description = "Friends"