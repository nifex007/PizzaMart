from django.db import models

# Create your models here.
class Orders(models.Model):

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
    flavour = models.CharField(choices=PIZZA_FLAVOURS, null=False, blank=False)
    size = models.CharField(choices=PIZZA_SIZES, null=False, blank=False)
    count = models.IntegerField(default=1, blank=False, null=False)
    order_status = models.CharField(choices=ORDER_STATUSES)

    def is_delivered(self):
        return self.order_status == 'DELIVERED'
    

    



