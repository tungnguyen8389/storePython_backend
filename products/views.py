from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .services import ProductService
from .serializers import ProductSerializer
from .models import Product
from rest_framework.permissions import AllowAny
from users.permissions import IsAdmin

class ProductListView(APIView):
    # Chỉ yêu cầu xác thực và admin cho POST
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_permissions(self):
        # Cho phép GET không yêu cầu xác thực
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()


    def get(self, request):
        # GET không yêu cầu phân quyền, cho phép tất cả người dùng
        products = Product.objects.all().select_related('category')
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        # Chỉ admin có thể tạo sản phẩm
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            product = ProductService.create_product(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    # Chỉ yêu cầu xác thực và admin cho PUT và DELETE
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_permissions(self):
        # Cho phép GET không yêu cầu xác thực
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, product_id):
        # GET không yêu cầu phân quyền
        product = ProductService.get_product_by_id(product_id)
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)

    def put(self, request, product_id):
        # Chỉ admin có thể cập nhật sản phẩm
        serializer = ProductSerializer(data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            product = ProductService.update_product(product_id, serializer.validated_data)
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        # Chỉ admin có thể xóa sản phẩm
        product = ProductService.get_product_by_id(product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)