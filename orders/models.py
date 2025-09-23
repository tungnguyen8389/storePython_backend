from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("BANK", "Bank Transfer"),
        ("CARD", "Credit/Debit Card"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="COD")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    # Danh sách sản phẩm lưu JSON: [{product_id, name, price, quantity}]
    items = models.JSONField(default=list)

    def __str__(self):
        return f"Order {self.id} - {self.user} - {self.total_price}"

    class Meta:
        ordering = ["-created_at"]
