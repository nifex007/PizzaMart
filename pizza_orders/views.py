from django.shortcuts import render
from rest_framework import viewsets
from pizza_orders.models import Order
from pizza_orders.serializers import OrderSerializer

# Create your views here.
class OrderReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
