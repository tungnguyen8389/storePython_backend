from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def list_cart_items(user):
    cart = get_or_create_cart(user)
    return cart.items.all()

def add_cart_item(user, product_id, quantity=1):
    cart = get_or_create_cart(user)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    return item

def update_cart_item(user, item_id, quantity):
    cart = get_or_create_cart(user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.quantity = quantity
    item.save()
    return item

def remove_cart_item(user, item_id):
    cart = get_or_create_cart(user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return True

def clear_cart(user):
    cart = get_or_create_cart(user)
    cart.items.all().delete()
    return True
