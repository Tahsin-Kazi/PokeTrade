from django.contrib import admin
from .models import Trade

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status',)
    search_fields = ('sender__user__username', 'receiver__user__username')
    list_per_page = 30
    list_select_related = ('sender', 'receiver')