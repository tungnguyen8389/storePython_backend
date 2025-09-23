from .models import Cart
from django.shortcuts import get_object_or_404

def get_all_carts(user=None):
    if user and not user.is_staff:
        return Cart.objects.filter(user=user)
    return Cart.objects.all()

def get_cart_by_id(pk):
    return get_object_or_404(Cart, pk=pk)

def create_cart(user, data):
    # Nếu đã có product trong giỏ -> tăng số lượng
    cart, created = Cart.objects.get_or_create(
        user=user, product=data["product"],
        defaults={"quantity": data.get("quantity", 1)}
    )
    if not created:
        cart.quantity += data.get("quantity", 1)
        cart.save()
    return cart

def update_cart(cart, data):
    for field, value in data.items():
        setattr(cart, field, value)
    cart.save()
    return cart

def delete_cart(cart):
    cart.delete()
