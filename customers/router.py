from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers.views import CustomerViewSet


router = DefaultRouter()
router.register(r'customers',  CustomerViewSet, basename='customer')