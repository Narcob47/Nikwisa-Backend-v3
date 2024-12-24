from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from categories.models import Category
# from weddings.models import WeddingsCategory

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('merchant', 'Merchant'),
        ('tasker', 'Tasker'),
        ('superuser', 'Superuser'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username
    
    
class Store(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type__in': ['merchant', 'tasker']})
    categories = models.ManyToManyField(Category, related_name='stores', blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    overview = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    whats_app = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)  # Add the store field

    def __str__(self):
        return f"{self.user.username} likes {self.store.name}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StoreImage(models.Model):
    store = models.ForeignKey(Store, related_name="extra_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="store_images/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.store.name}"

class StoreReview(models.Model):
    store = models.ForeignKey(Store, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating scale (e.g., 1-5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.store}"

class Reaction(models.Model):
    store = models.ForeignKey(Store, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="store_likes", on_delete=models.CASCADE)  # Use a unique related_name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.store.name}"

class Offering(models.Model):
    store = models.ForeignKey(Store, related_name="store_offerings", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    wedding_category = models.ForeignKey('weddings.WeddingsCategory', related_name="wedding_offerings", on_delete=models.SET_NULL, blank=True, null=True)  # Use string reference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name