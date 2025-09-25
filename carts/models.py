from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),          # đang dùng
        ("checked_out", "Checked Out"),# đã thanh toán
        ("abandoned", "Abandoned"),    # bỏ dở
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user} ({self.status})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
