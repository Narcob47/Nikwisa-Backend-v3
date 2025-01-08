from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.text import slugify
from store.models import Store  

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('merchant', 'Merchant'),
        ('tasker', 'Tasker'),
        ('superuser', 'Superuser'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)  # Allow blank and null values
    # phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    
    # Update related_name for groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(Group, related_name='store_customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='store_customuser_permissions', blank=True)
    
    def __str__(self):
        return self.username
    
class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_like_set')  # Changed related_name

    def __str__(self):
        return f"{self.user.username} likes {self.store.name}"