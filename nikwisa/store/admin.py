from django.contrib import admin
from .models import Store, Review, Like

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    search_fields = ('name', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories', 'products')

admin.site.register(Store, StoreAdmin)
admin.site.register(Review)
admin.site.register(Like)