from django.shortcuts import render
from rest_framework import viewsets
from customers.models import Customer
from customers.serializers import CustomerSerializer

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing customer instances.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

