from rest_framework import serializers
from .models import User, Product, CartItem, Order, ProductOrder

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'fullname', 'email', 'role', 'address', 'tel']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image']


class ProductOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = ProductOrder
        fields = ['product_name', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_date', 'status', 'total_price', 'items']

    def get_items(self, obj):
        product_orders = ProductOrder.objects.filter(order=obj)
        return ProductOrderSerializer(product_orders, many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    description = serializers.CharField(source='product.description')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    available = serializers.IntegerField(source='product.stock')
    imageUrl = serializers.ImageField(source='product.image')

    class Meta:
        model = CartItem
        fields = ['id', 'name', 'description', 'price', 'quantity', 'available', 'imageUrl']
