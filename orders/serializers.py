from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "user", "total_price", "status", 
            "payment_method", "payment_status", 
            "items", "created_at"
        ]
