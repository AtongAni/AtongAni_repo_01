from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        FARMER = 'FARMER', 'Farmer'
        ADMIN = 'ADMIN', 'Admin'
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)  



class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
related_name = 'farmer_profile')
    farm_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    is_approved = models.BooleanField(default=False) # optional but recommended 

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
related_name = 'customer_profile')
    phone = models.CharField(max_length=30, blank=True)

