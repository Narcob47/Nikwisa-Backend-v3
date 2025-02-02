from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Message, Like, Review, StoredJWT

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('id',)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'profile_image', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)

# Message Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp',)

admin.site.register(Message, MessageAdmin)

# Like Admin
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'target_user', 'created_at')
    search_fields = ('user__username', 'target_user__username')
    list_filter = ('created_at',)

admin.site.register(Like, LikeAdmin)

# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reviewed_user', 'rating', 'comment', 'created_at')
    search_fields = ('user__username', 'reviewed_user__username', 'comment')
    list_filter = ('rating', 'created_at')

admin.site.register(Review, ReviewAdmin)

# StoredJWT Admin
class StoredJWTAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'refresh_token', 'created_at')
    search_fields = ('user__username', 'access_token', 'refresh_token')
    list_filter = ('created_at',)

admin.site.register(StoredJWT)