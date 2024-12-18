from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from categories.models import Category
from products.models import CentralizedProduct

User = get_user_model()

class Store(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type__in': ['merchant', 'tasker']})
    categories = models.ManyToManyField(Category, related_name='stores', blank=True)
    products = models.ManyToManyField(CentralizedProduct, related_name='stores', blank=True)
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

class StoreImage(models.Model):
    store = models.ForeignKey(Store, related_name="extra_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="store_images/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.store.name}"

class Review(models.Model):
    store = models.ForeignKey(Store, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating scale (e.g., 1-5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.store}"

class Like(models.Model):
    store = models.ForeignKey(Store, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="store_likes", on_delete=models.CASCADE)  # Use a unique related_name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.store.name}"