from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CartSerializer
from .services import get_all_carts, get_cart_by_id, create_cart, update_cart, delete_cart

class CartListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = get_all_carts(request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            cart = create_cart(request.user, serializer.validated_data)
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        cart = get_cart_by_id(pk)
        return Response(CartSerializer(cart).data)

    def put(self, request, pk):
        cart = get_cart_by_id(pk)
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            updated_cart = update_cart(cart, serializer.validated_data)
            return Response(CartSerializer(updated_cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = get_cart_by_id(pk)
        delete_cart(cart)
        return Response(status=status.HTTP_204_NO_CONTENT)
