from django.shortcuts import render
from rest_framework import viewsets
from customers.models import Customer
from customers.serializers import CustomerSerializer
from pizza_mart.utils import Pagination

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing customer instances.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    pagination_class = Pagination

