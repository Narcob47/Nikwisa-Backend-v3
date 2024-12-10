from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import CentralizedProduct
from products.models import YourProductModel  # Replace with your actual product model

@receiver(post_save, sender=YourProductModel)
def create_centralized_product(sender, instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(instance)
        CentralizedProduct.objects.create(
            content_type=content_type,
            object_id=instance.id,
            content_object=instance
        )