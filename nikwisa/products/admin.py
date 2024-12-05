from django.contrib import admin
from .models import CentralizedProduct

# from .models import CentralizedProduct

# class CentralizedProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'subcategory', 'price')
#     search_fields = ('name', 'category__title', 'subcategory__title')
#     list_filter = ('category', 'subcategory')

# admin.site.register(CentralizedProduct, CentralizedProductAdmin)
admin.site.register(CentralizedProduct)