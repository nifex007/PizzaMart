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
from pizza_mart.utils import Pagination
from rest_framework.decorators import action
from django.shortcuts import redirect


# Create your views here.
class OrderReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing Orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_status', 'customer']
    pagination_class = Pagination


class OrderViewSet(viewsets.ModelViewSet):
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
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'error': error.detail},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def update(self, request, pk=None):
        order = self.get_object(pk)
        serializer = self.serializer_class(order, data=request.data)
        if serializer.is_valid():
            # prevent update when pizza is delivered
            if order.is_delivered():
                return Response({'message': 'Pizza already delivered to {} at {}'.format(order.customer.full_name,
                                                                                         order.customer.address)},
                                status=status.HTTP_400_BAD_REQUEST)
            # prevent update when pizza is in transit
            elif order.is_in_transit():
                return Response({'message': 'Pizza already in Transit to {} for {}'.format(order.customer.address,
                                                                                           order.customer.full_name
                                                                                           )},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        order = self.get_object(pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)

        if serializer.is_valid():
            payload_order_status = request.data.get('order_status', None)
            if order.is_delivered():
                return Response({'message': 'Pizza already delivered to {} at {}'.format(order.customer.full_name,
                                                                                         order.customer.address)},
                                status=status.HTTP_400_BAD_REQUEST)

            elif order.is_in_transit() and payload_order_status is not None:
                # allow update only on order_status field
                delivered_status = {"order_status": payload_order_status}
                serializer_ = self.serializer_class(order, data=delivered_status, partial=True)
                if serializer_.is_valid():
                    serializer_.save()
                    order.delivery_date = timezone.now()
                    order.save()
                    return Response(serializer.data)
                return Response(serializer_.errors, status=status.HTTP_400_BAD_REQUEST)

            elif order.is_in_transit() and payload_order_status is None:
                return Response({'message': 'Pizza already in Transit to {} for {}'
                                .format(order.customer.address, order.customer.full_name)},
                                status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        order = self.get_object(pk)

        order_status = {
            "order_id": order.id,
            "order_destination": order.customer.address,
            "order_status": order.order_status,
        }
        return Response(order_status)

    def list(self, request):
        return redirect('/api/orders-list/')
