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
            self.slug = slugify(self.name)
        super(WeddingsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class WeddingSubCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    categories = models.ManyToManyField(WeddingsCategory, related_name='subcategories', blank=True)
    image = models.ImageField(upload_to='weddings_subcategories/', blank=True, null=True)  # Image field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(WeddingSubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Weddings(models.Model):
    category = models.ForeignKey(WeddingsCategory, related_name='weddings', on_delete=models.CASCADE, blank=True)
    subcategory = models.ForeignKey(WeddingSubCategory, related_name='weddings', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='weddings/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if isinstance(self.date, str):
            self.date = parse_date(self.date)
        super(Weddings, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
