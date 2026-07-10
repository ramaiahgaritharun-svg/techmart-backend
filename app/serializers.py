from rest_framework import serializers
from app.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "user",
            "product",
            "product_id",
            "created_at",
        ]

        extra_kwargs = {"user": {"read_only": True}}


class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)

    product_price = serializers.FloatField(source="product.price", read_only=True)

    product_image = serializers.ImageField(source="product.image", read_only=True)

    product_stock = serializers.IntegerField(source="product.stock", read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"

        extra_kwargs = {"cart": {"required": False, "read_only": True}}


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

        extra_kwargs = {
            "user": {"required": False, "read_only": True},
            "full_name": {"required": False},
            "email": {"required": False},
            "mobile": {"required": False},
            "address": {"required": False},
        }
