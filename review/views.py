from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import ReviewSerializer
from .services import get_reviews_for_product, create_review, get_review_by_id, update_review, delete_review
from users.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated 

class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Cho phép GET không yêu cầu xác thực
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, product_id):
        reviews = get_reviews_for_product(product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        data = request.data.copy()
        data["product"] = product_id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            review = create_review(request.user, serializer.validated_data)
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        review = get_review_by_id(pk)
        return Response(ReviewSerializer(review).data)

    def put(self, request, pk):
        review = get_review_by_id(pk)
        if review.user != request.user:
            return Response({"error": "Bạn không thể sửa review của người khác"}, status=403)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            updated = update_review(review, serializer.validated_data)
            return Response(ReviewSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = get_review_by_id(pk)
        if review.user != request.user:
            return Response({"error": "Bạn không thể xóa review của người khác"}, status=403)
        delete_review(review)
        return Response(status=status.HTTP_204_NO_CONTENT)
