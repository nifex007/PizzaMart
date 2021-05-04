from rest_framework import serializers
from pizza_orders.models import Order
from customers.models import Customer
from customers.serializers import CustomerSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Read, Edit & Delete Orders
    """
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
