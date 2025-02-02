from django.contrib.auth.models import AbstractUser
from django.db import models
from store.models import Store, Offering, StoreReview

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('merchant', 'Merchant'),
        ('superuser', 'Superuser'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    user_type = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_merchant(self):
        return self.role == 'merchant'

    def is_client(self):
        return self.role == 'client'  

class StoredJWT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="jwt_token")
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"JWT for {self.user.username}"
    
# Message Model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

# Like Model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target_user')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user} liked {self.target_user}"

# Review Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reviewed_user')  # One review per user

    def __str__(self):
        return f"Review by {self.user}"
