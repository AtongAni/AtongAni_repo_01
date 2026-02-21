from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    UNIT_CHOICES = [
        ('KG', 'Kilogram'),
        ('G', 'Gram'),
    ]
    
    POST_TYPE_CHOICES = [
        ('DEFAULT', 'Default Post'),
        ('HARVEST_FORECAST', 'Harvest Forecast'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True, help_text="Primary product image (deprecated - use images relation)")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Available quantity")
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='KG', help_text="Unit of measurement")
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='DEFAULT', help_text="Type of post")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/', help_text="Product image")
    order = models.PositiveIntegerField(default=0, help_text="Image display order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.post.title} - Image {self.order + 1}"


class FarmerHarvestProfile(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REVISION_REQUESTED', 'Revision Requested'),
    ]
    
    farmer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='harvest_profile')
    land_size = models.DecimalField(max_digits=8, decimal_places=2, help_text="Land size in hectares")
    land_size_unit = models.CharField(max_length=20, default='hectares', help_text="Unit of measurement for land size")
    crop_type = models.CharField(max_length=255, help_text="Type of crop/crops being grown")
    previous_harvest_quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Quantity from previous harvest")
    previous_harvest_unit = models.CharField(max_length=20, default='KG', help_text="Unit for previous harvest")
    previous_harvest_date = models.DateField(blank=True, null=True, help_text="Date of previous harvest")
    farming_experience_years = models.PositiveIntegerField(blank=True, null=True, help_text="Years of farming experience")
    location = models.CharField(max_length=255, blank=True, help_text="Farm location")
    notes = models.TextField(blank=True, help_text="Additional notes or farming details")
    
    # Approval status
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Admin review notes")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_farmers', help_text="Admin who approved this profile")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Farmer Harvest Profile"
        verbose_name_plural = "Farmer Harvest Profiles"
    
    def __str__(self):
        return f"{self.farmer.username} - {self.status}"
    
    def is_verified(self):
        """Check if farmer's harvest forecast profile is approved"""
        return self.status == 'APPROVED'
