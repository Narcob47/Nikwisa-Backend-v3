from django.contrib import admin
from .models import Store, StoreReview, Reaction, Offering

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    search_fields = ('name', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)

class OfferingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    search_fields = ('name', 'description')
    list_filter = ('name',)

admin.site.register(Store, StoreAdmin)
admin.site.register(StoreReview)
admin.site.register(Reaction)
admin.site.register(Offering, OfferingAdmin)
