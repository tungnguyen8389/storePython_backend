from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from .models import Product, Category

class ProductService:
    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

    @staticmethod
    def create_product(data):
        category_id = data.get("category")
        if not category_id:
            raise ValidationError("Category is required")

        try:
            category = Category.objects.get(id=category_id.id if hasattr(category_id, 'id') else category_id)
        except Category.DoesNotExist:
            raise ValidationError("Invalid category")

        product = Product.objects.create(**data)
        return product

    @staticmethod
    def update_product(product_id, data):
        product = ProductService.get_product_by_id(product_id)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def check_stock(product_id, quantity):
        product = ProductService.get_product_by_id(product_id)
        if product.stock_quantity < quantity:
            raise ValidationError(f"Only {product.stock_quantity} items in stock")
        return product