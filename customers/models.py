from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Customer(AbstractUser):
    full_name = models.CharField(max_length=255)
    address = models.TextField(blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    phone = models.CharField(max_length=14, blank=False, null=False, unique=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    def __str__(self):
        return '{} - {}'.format(self.full_name, self.phone)