from django.shortcuts import render
from rest_framework import viewsets
from pizza_orders.models import Order
from pizza_orders.serializers import OrderSerializer, OrderCreateSerializer
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

# Create your views here.
class OrderReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing Orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_status', 'customer']


class OrderViewSet(viewsets.ViewSet):
    """
    A viewset for creating, editing and deleting order instances.
    """
    serializer_class = OrderSerializer


    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404
   
    def create(self, request, *args, **kwargs):
        try:
            serializer = OrderCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'error': error.detail}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        order = self.get_object(pk)
        serializer = self.serializer_class(order, data=request.data)
        if serializer.is_valid():
            # prevent update when pizza is delivered
            if order.is_delivered():
                return Response({'message': 'Pizza already delivered to {} at {}'. format(order.customer.full_name, order.customer.address)}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('order_status', None) == 'DELIVERED': 
                serializer.save()
                order.delivery_date = timezone.now()
                order.save()
                return Response(serializer.data)
            else:
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        order = self.get_object(pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    



