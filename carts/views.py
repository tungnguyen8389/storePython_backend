from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CartSerializer, CartItemSerializer
from .services import (
    get_or_create_cart, list_cart_items, add_cart_item,
    update_cart_item, remove_cart_item, clear_cart
)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        item = add_cart_item(request.user, product_id, quantity)
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        quantity = int(request.data.get("quantity", 1))
        item = update_cart_item(request.user, item_id, quantity)
        return Response(CartItemSerializer(item).data)


class CartItemRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        remove_cart_item(request.user, item_id)
        return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)


class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        clear_cart(request.user)
        return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)
