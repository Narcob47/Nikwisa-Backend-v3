from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and all permissions.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)  # Make sure to set this to True
        extra_fields.setdefault('role', 'client')  # Set a default role, you can adjust this

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('merchant', 'Merchant'),
    ]
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    
    # Explicitly define the is_staff and is_active fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # This is a list of fields that are required when creating a superuser

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    user_type = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_merchant(self):
        return self.role == 'merchant'

    def is_client(self):
        return self.role == 'client'

    def __str__(self):
        return self.username



class StoredJWT(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="jwt_token")
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"JWT for {self.user.username}"
    
# Message Model
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

# Like Model
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target_user')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user} liked {self.target_user}"

# Review Model
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(CustomUser, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reviewed_user')  # One review per user

    def __str__(self):
        return f"Review by {self.user}"
