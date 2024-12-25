from django.contrib import admin
from .models import Store, StoreReview, Reaction, Offering

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    search_fields = ('name', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)

class OfferingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'store', 'phone_number', 'whatsapp_number']
    search_fields = ['name', 'description', 'phone_number', 'whatsapp_number']
    list_filter = ('name',)

admin.site.register(Store, StoreAdmin)
admin.site.register(StoreReview)
admin.site.register(Reaction)
admin.site.register(Offering, OfferingAdmin)
