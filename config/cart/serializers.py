from rest_framework import serializers
from .models import Cart, CartItem
from typing import Any

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'quantity',
            'total_price'
        ]

    def get_total_price(self, obj: CartItem) -> float:
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'cart_total']

    def get_cart_total(self, obj: Cart) -> float:
        return sum(item.get_total_price() for item in obj.items.all())


class RemoveCartItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
