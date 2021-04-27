from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order
from order.serializers import OrderModelSerializer, Order2ModelSerializer


class OrderAPIView(CreateAPIView):
    """订单的视图"""
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = OrderModelSerializer

class OrderListAPIView(ListAPIView):
    """订单的视图"""
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = Order2ModelSerializer


class OrderSiteAPIView(APIView):

    def get(self, request):
        order_number = request.query_params.get("order_number")
        connection = get_redis_connection("order_site")
        site = connection.get(f"site_{order_number}")
        if not site:
            return Response({"message": "订单已过期或不存在"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"site": site})