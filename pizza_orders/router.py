from rest_framework.routers import DefaultRouter
from pizza_orders.views import OrderReadOnlyViewSet


router = DefaultRouter()
router.register(r'orders', OrderReadOnlyViewSet, basename='read_order')