from django.contrib import admin
from .models import Store, StoreReview, Reaction, Offering, StoreImage

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    search_fields = ('name', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)

class OfferingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'store', 'phone_number', 'whatsapp_number']
    search_fields = ['name', 'description', 'phone_number', 'whatsapp_number']
    list_filter = ('name',)

class StoreImageAdmin(admin.ModelAdmin):
    list_display = ['store', 'image', 'uploaded_at']
    search_fields = ['store__name', 'store__owner__username']  # To search images by associated store
    list_filter = ['uploaded_at']

admin.site.register(Store, StoreAdmin)
admin.site.register(StoreReview)
admin.site.register(Reaction)
admin.site.register(Offering, OfferingAdmin)
admin.site.register(StoreImage, StoreImageAdmin)  # Register StoreImage model
