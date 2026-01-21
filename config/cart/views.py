from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product

@extend_schema(
    responses={200: CartSerializer}
)
class CartDetailView(APIView):
    def get(self, request):
        cart = (
            Cart.objects
            .select_related('user')
            .prefetch_related('items__product')
            .get(user=request.user)
            )
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartRequestSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

@extend_schema(
    tags=['Cart'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'product_id': {'type': 'integer'},
                'quantity': {'type': 'integer'},
            }
        }
    },
    responses={200: {'message': 'Product added to cart'}}
)

class AddToCartView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        # ✅ EDGE CASE 1: Invalid quantity
        if quantity <= 0:
            return Response(
                {'error': 'Quantity must be greater than zero'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ EDGE CASE 2: Invalid product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Invalid product'},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ EDGE CASE 3: Inactive product
        if not product.is_active:
            return Response(
                {'error': 'Product not available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ EDGE CASE 4: Stock check
        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart.objects.get(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        # ✅ EDGE CASE 5: Quantity overflow
        if not created and cart_item.quantity + quantity > product.stock:
            return Response(
                {'error': 'Exceeds available stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'message': 'Product added to cart'})

class UpdateCartItemRequestSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

class UpdateCartItemResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class UpdateCartItemErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

@extend_schema(
    request=UpdateCartItemRequestSerializer,
    responses={
        200: UpdateCartItemResponseSerializer,
        400: UpdateCartItemErrorSerializer
    }
)

class UpdateCartItemView(APIView):
    def patch(self, request, item_id):
        quantity = int(request.data.get('quantity'))

        # ✅ EDGE CASE 1: Invalid quantity
        if quantity <= 0:
            return Response(
                {'error': 'Quantity must be greater than zero'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ EDGE CASE 2: Stock check
        if cart_item.product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response({'message': 'Cart updated'})


from rest_framework.generics import GenericAPIView
from .serializers import RemoveCartItemSerializer
class RemoveCartItemView(GenericAPIView):
    serializer_class = RemoveCartItemSerializer

    def delete(self, request):
        item_id = request.data.get('item_id')
        cart_item = CartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )
        cart_item.delete()
        return Response({'message': 'Cart item removed'})



