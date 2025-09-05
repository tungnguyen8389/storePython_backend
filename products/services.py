from .models import Product

def get_all_products():
    return Product.objects.all()

def create_product(validated_data):
    return Product.objects.create(**validated_data)

def update_product(product, validated_data):
    for attr, value in validated_data.items():
        setattr(product, attr, value)
    product.save()
    return product

def delete_product(product):
    product.delete()
