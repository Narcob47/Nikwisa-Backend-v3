from django.contrib import admin
from .models import Store

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    search_fields = ('name', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories', 'products')

admin.site.register(Store, StoreAdmin)