from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Message, Like, PhoneNumber

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'profile_image', )  # Added phone_number
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')  # Included phone_number in search
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'groups')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}), 
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_image', )}),  # Added phone_number
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
        ('Important dates', {'fields': ('last_login', 'date_joined')}), 
        ('User Type', {'fields': ('user_type',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'profile_image', ),  # Added phone_number
        }),
    )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'store')  # Corrected field name
    list_filter = ('user', 'store')   # Corrected field name
    search_fields = ('user__username', 'store__name')  # Corrected field name

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'verified')
    search_fields = ('phone_number',)
    list_filter = ('verified',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Like, LikeAdmin)
