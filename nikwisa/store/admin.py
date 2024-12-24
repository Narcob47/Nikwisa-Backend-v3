from django.contrib import admin
from .models import Store, StoreReview, Reaction, Offering

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    search_fields = ('name', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)  # Add a comma to make it a tuple
    
    
class OfferingAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'store__name')
    list_filter = ('store', 'created_at', 'updated_at')

admin.site.register(Store, StoreAdmin)
admin.site.register(StoreReview)
admin.site.register(Reaction)
admin.register(Offering)
