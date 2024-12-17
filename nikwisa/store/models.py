from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from categories.models import Category
from products.models import CentralizedProduct

User = get_user_model()

class Store(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type__in': ['merchant', 'tasker']})
    categories = models.ManyToManyField(Category, related_name='stores')
    products = models.ManyToManyField(CentralizedProduct, related_name='stores')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    overview = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    whats_app = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on object creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated on save

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
