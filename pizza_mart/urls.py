"""pizza_mart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from customers.views import CustomerViewSet
from pizza_mart.views import index
from pizza_orders.views import OrderReadOnlyViewSet, OrderViewSet


main_router = routers.DefaultRouter()

main_router.register(r'customers/?', CustomerViewSet, basename='customer')
main_router.register(r'orders-list/?', OrderReadOnlyViewSet, basename='orders')
main_router.register(r'orders/?', OrderViewSet, basename='order')

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include(main_router.urls)),
    
    
]
