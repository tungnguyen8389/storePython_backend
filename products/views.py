from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsAdmin
from .models import Product
from .serializers import ProductSerializer
from .services import get_all_products, create_product, update_product, delete_product

class ProductListView(APIView):
    permission_classes = [AllowAny]   # ai cũng xem được

    def get(self, request):
        products = get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = create_product(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated_product = update_product(product, serializer.validated_data)
            return Response(ProductSerializer(updated_product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        delete_product(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
