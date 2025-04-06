from django.contrib import admin

from django.db.models.functions import Lower


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('friend', 'name', 'owner', 'id')
    search_fields = ('name')
    list_filter = ('date_found')
    list_per_page = 30

    fields = ('friend', 'name', 'owner', 'data')
    readonly_fields = ('data')

    def save_model(self, request, obj, form, change):
        if not obj.name:
            obj.name = obj.data.get('name')

        obj.save()
        super().save_model(request, obj, form, change)