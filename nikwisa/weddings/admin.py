from django.contrib import admin
from .models import Weddings

class WeddingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'date', 'location')
    search_fields = ('title', 'category__name', 'subcategory__name', 'location')
    list_filter = ('category', 'subcategory', 'date')

admin.site.register(Weddings, WeddingsAdmin)
