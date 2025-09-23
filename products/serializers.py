from rest_framework import serializers
from .models import Product, Category
from categories.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    image_url = serializers.SerializerMethodField(read_only=True)  # để trả về link ảnh đầy đủ

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'description',
            'price', 'stock', 'image', 'image_url', 'created_at'
        ]
        extra_kwargs = {"image": {"write_only": True}}  # chỉ dùng khi upload

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None