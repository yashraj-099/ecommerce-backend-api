from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer

from django.db.models import F



class CreateOrderSuccessSerializer(serializers.Serializer):
    message = serializers.CharField()
    order_id = serializers.IntegerField()

class CreateOrderErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

@extend_schema(
    responses={
        201: CreateOrderSuccessSerializer,
        400: CreateOrderErrorSerializer
    }
)

class CreateOrderView(APIView):
    def post(self, request):
        cart = Cart.objects.get(user=request.user)

        # ✅ EDGE CASE 1: Empty cart
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ EDGE CASE 2: Existing pending order
        if Order.objects.filter(user=request.user, status='PENDING').exists():
            return Response(
                {'error': 'Complete pending order first'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            product.stock = F('stock') - item.quantity
            product.save()
            product.refresh_from_db()



@extend_schema(
    responses={200: OrderSerializer(many=True)}
)
class MyOrdersView(APIView):
    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .select_related('user')
            .prefetch_related('items__product')
            .order_by('-created_at')
            )

        from .serializers import OrderSerializer
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
