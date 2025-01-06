from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import CentralizedProduct
from weddings.models import Weddings  # Import the Weddings model

# @receiver(post_save, sender=CentralizedProduct)
# def create_centralized_product(sender, instance, created, **kwargs):
#     if created:
#         content_type = ContentType.objects.get_for_model(instance)
#         CentralizedProduct.objects.create(
#             content_type=content_type,
#             object_id=instance.id,
#             content_object=instance
#         )

@receiver(post_save, sender=Weddings)
def create_centralized_product(sender, instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(instance)
        CentralizedProduct.objects.create(
            content_type=content_type,
            object_id=instance.id,
            content_object=instance
        )