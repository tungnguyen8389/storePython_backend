from django.db import transaction
from carts.models import Cart
from .models import Order, OrderItem
from products.models import Product


def checkout_cart(user, payment_method="cod"):
    cart = Cart.objects.filter(user=user, status="active").first()
    if not cart or cart.items.count() == 0:
        raise ValueError("Cart is empty")

    with transaction.atomic():
        total = sum(item.product.price * item.quantity for item in cart.items.all())

        order = Order.objects.create(
            user=user,
            total_price=total,
            payment_method=payment_method,
            status="pending"
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.status = "checked_out"
        cart.save()
        cart.items.all().delete()

    return order
