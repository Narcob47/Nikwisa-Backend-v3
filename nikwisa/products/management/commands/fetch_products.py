# Create a management command in your app (e.g., `management/commands/fetch_products.py`)

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from products.models import CentralizedProduct  # Replace `myapp` with your app name
from weddings.models import Weddings as Product1  # Replace `app1` with your app name
# from app2.models import Product as Product2  # Replace `app2` with your app name

class Command(BaseCommand):
    help = 'Fetch products from different apps and store them in the centralized product model'

    def handle(self, *args, **kwargs):
        self.fetch_products(Product1)
        # self.fetch_products(Product2)
        self.stdout.write(self.style.SUCCESS('Successfully fetched products'))

    def fetch_products(self, product_model):
        content_type = ContentType.objects.get_for_model(product_model)
        products = product_model.objects.all()
        for product in products:
            CentralizedProduct.objects.get_or_create(
                content_type=content_type,
                object_id=product.id,
                defaults={'content_object': product}
            )