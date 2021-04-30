from django.db import models
from customers.models import Customer

# Create your models here.
class Order(models.Model):

    PIZZA_FLAVOURS = [
        ('MARGARITA', 'margarita'),
        ('MARINARA', 'marinara'),
        ('SALAMI', 'salami'),
    ]

    PIZZA_SIZES = [
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
    ]

    ORDER_STATUSES = [
        ('RECIEVED', 'recieved'),
        ('TRANSIT', 'transit'),
        ('DELIVERED', 'delivered'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    flavour = models.CharField(max_length=10, choices=PIZZA_FLAVOURS, null=False, blank=False)
    size = models.CharField(max_length=6, choices=PIZZA_SIZES, null=False, blank=False)
    count = models.IntegerField(default=1, blank=False, null=False)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUSES)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    

    def is_delivered(self):
        return self.order_status == 'DELIVERED'
    

    



