from django.db import models
from django.utils.text import slugify
from django.utils.dateparse import parse_date
from django.contrib.auth import get_user_model

User = get_user_model()

class WeddingsCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='weddings_categories/', blank=True, null=True)  # Image field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(WeddingsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class WeddingSubCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(WeddingsCategory, related_name='subcategories')

    def __str__(self):
        return self.title
