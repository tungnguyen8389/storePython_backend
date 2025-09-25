from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from categories.models import Category
from categories.services import CategoryService
from categories.serializers import CategorySerializer
from users.permissions import IsAdmin

class CategoryListView(APIView):
    # Mặc định yêu cầu xác thực và admin cho POST
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_permissions(self):
        # Cho phép GET không yêu cầu xác thực
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request):
        categories = CategoryService.get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Chỉ admin có thể tạo danh mục
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = CategoryService.create_category(serializer.validated_data)
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    # Mặc định yêu cầu xác thực và admin cho PUT và DELETE
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_permissions(self):
        # Cho phép GET không yêu cầu xác thực
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, category_id):
        category = CategoryService.get_category_by_id(category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, category_id):
        # Chỉ admin có thể cập nhật danh mục
        serializer = CategorySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            category = CategoryService.update_category(category_id, serializer.validated_data)
            return Response(CategorySerializer(category).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        # Chỉ admin có thể xóa danh mục
        CategoryService.delete_category(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)