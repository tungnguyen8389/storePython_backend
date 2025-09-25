from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("bank", "Bank Transfer"),
        ("card", "Credit/Debit Card"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cod")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"
