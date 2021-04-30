from rest_framework import serializers
from pizza_orders.models import Order
from customers.serializers import CustomerSerializer

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

