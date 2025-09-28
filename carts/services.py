from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from carts.models import Cart, CartItem
from django.db import transaction

# def get_or_create_cart(user):
#     cart, created  = Cart.objects.get_or_create(user=user)
#     if created:
#         cart.status = "active"
#         cart.save()
#     return cart

# def get_or_create_cart(user):
#     cart, created = Cart.objects.get_or_create(user=user, defaults={'status': 'active'})
#     return cart

@transaction.atomic 
def get_or_create_cart(user):
    # 1. Cố gắng tìm giỏ hàng active (dạng đang hoạt động)
    active_cart = Cart.objects.filter(user=user, status="active").first()
    
    if active_cart:
        return active_cart
    
    existing_cart = Cart.objects.filter(user=user).order_by('-updated_at').first()
    if existing_cart and existing_cart.status != "active":
        if existing_cart.status == "checked_out":
             existing_cart.items.all().delete() 
        existing_cart.status = "active"
        existing_cart.save()
        
        return existing_cart

    new_cart = Cart.objects.create(user=user, status="active")
    return new_cart

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
