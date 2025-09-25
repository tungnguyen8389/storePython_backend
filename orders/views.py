from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import OrderSerializer
from .services import checkout_cart
from .models import Order
from users.permissions import IsAdmin  # custom permission cho admin


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_method = request.data.get("payment_method", "cod")
        try:
            order = checkout_cart(request.user, payment_method)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admin thấy tất cả đơn hàng, user chỉ thấy của mình
        if request.user.is_staff:
            orders = Order.objects.all().prefetch_related("items")
        else:
            orders = Order.objects.filter(user=request.user).prefetch_related("items")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, order_id):
        try:
            order = Order.objects.prefetch_related("items").get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return Response({"message": "Order deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
