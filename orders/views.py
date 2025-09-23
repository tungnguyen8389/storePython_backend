from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import OrderSerializer
from .services import get_all_orders, get_order_by_id, create_order, update_order, delete_order
from .models import Order

class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = get_all_orders(request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = create_order(request.user, serializer.validated_data)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_order_by_id(pk)
        return Response(OrderSerializer(order).data)

    def put(self, request, pk):
        order = get_order_by_id(pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            updated_order = update_order(order, serializer.validated_data)
            return Response(OrderSerializer(updated_order).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = get_order_by_id(pk)
        delete_order(order)
        return Response(status=status.HTTP_204_NO_CONTENT)
