from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1–5 sao

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")  # 1 user chỉ review 1 lần/1 product
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.product} ({self.rating}★)"
