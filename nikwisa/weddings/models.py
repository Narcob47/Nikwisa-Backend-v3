from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class WeddingsCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='weddings_categories/', blank=True, null=True)  # Image field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(WeddingsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class WeddingSubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    categories = models.ManyToManyField(WeddingsCategory, related_name='subcategories', blank=True)
    image = models.ImageField(upload_to='weddings_subcategories/', blank=True, null=True)  # Image field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(WeddingSubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Weddings(models.Model):
    product_title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    send_inquiry = models.ForeignKey(User, related_name='inquiries', on_delete=models.SET_NULL, blank=True, null=True)
    related_products = models.ManyToManyField('self', symmetrical=False, related_name='related_to', blank=True)
    reaction = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # Rating field
    category = models.ForeignKey(WeddingsCategory, related_name='weddings', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(WeddingSubCategory, related_name='weddings', on_delete=models.SET_NULL, blank=True, null=True)
    services = models.TextField(blank=True, null=True)  # Optional services field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_title)
        super(Weddings, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_title

    def get_related_products(self):
        return Weddings.objects.filter(category=self.category).exclude(id=self.id)
