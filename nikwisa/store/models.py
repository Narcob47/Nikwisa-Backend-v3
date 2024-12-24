from django.db import models
from django.utils.text import slugify
from categories.models import Category

class Store(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'user_type__in': ['merchant', 'tasker']})
    categories = models.ManyToManyField(Category, related_name='stores', blank=True)
    wedding_category = models.ForeignKey('weddings.WeddingsCategory', related_name="store_wedding_offerings", on_delete=models.SET_NULL, blank=True, null=True)
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
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="store_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="store_likes")
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.store.name}"

class StoreReview(models.Model):
    store = models.ForeignKey(Store, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="store_reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.store}"

class Reaction(models.Model):
    store = models.ForeignKey(Store, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", related_name="store_reactions", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.store.name}"

class Offering(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='offerings_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, related_name="offerings", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", related_name="offerings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name