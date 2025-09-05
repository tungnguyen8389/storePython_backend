from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Seed product data"

    def handle(self, *args, **kwargs):
        if not Product.objects.exists():
            Product.objects.create(name="Laptop Dell", description="Core i5, 8GB RAM", price=1200, stock=10)
            Product.objects.create(name="iPhone 14", description="128GB, màu đen", price=999, stock=5)
            Product.objects.create(name="Tai nghe Sony", description="Noise Cancelling", price=199, stock=20)
            self.stdout.write(self.style.SUCCESS("✅ Seeded sample products"))
