from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Message, Like

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('User Type', {'fields': ('user_type',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user', 'product')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Like, LikeAdmin)
