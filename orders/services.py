from .models import Order
from django.shortcuts import get_object_or_404

def get_all_orders(user=None):
    if user and not user.is_staff:
        return Order.objects.filter(user=user)
    return Order.objects.all()

def get_order_by_id(pk):
    return get_object_or_404(Order, pk=pk)

def create_order(user, data):
    if "user" in data:
        data.pop("user")
    return Order.objects.create(user=user, **data)

def update_order(order, data):
    for field, value in data.items():
        setattr(order, field, value)
    order.save()
    return order

def delete_order(order):
    order.delete()
