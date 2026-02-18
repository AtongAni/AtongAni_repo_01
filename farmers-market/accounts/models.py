from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        FARMER = 'FARMER', 'Farmer'
        RIDER = 'RIDER', 'Rider'
        ADMIN = 'ADMIN', 'Admin'
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    is_suspended = models.BooleanField(default=False)
    suspended_at = models.DateTimeField(null=True, blank=True)
    suspension_reason = models.TextField(blank=True)



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


class RiderProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rider_profile')
    phone = models.CharField(max_length=30, blank=True)
    vehicle_type = models.CharField(max_length=50, blank=True) # e.g., "motorcycle", "car", "bicycle"
    vehicle_plate = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_deliveries = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Rider"
