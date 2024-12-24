from django.contrib import admin
from .models import WeddingsCategory, WeddingSubCategory

class WeddingsCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

class WeddingSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'categories__title')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)

# class WeddingsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'subcategory', 'date', 'location')
#     search_fields = ('title', 'category__title', 'subcategory__title', 'location')
#     list_filter = ('category', 'subcategory', 'date')

admin.site.register(WeddingsCategory, WeddingsCategoryAdmin)
admin.site.register(WeddingSubCategory, WeddingSubCategoryAdmin)
# admin.site.register( WeddingsAdmin)
