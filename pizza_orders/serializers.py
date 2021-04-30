from rest_framework import serializers
from pizza_orders.models import Order

class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'