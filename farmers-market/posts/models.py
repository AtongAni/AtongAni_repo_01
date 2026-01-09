from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    UNIT_CHOICES = [
        ('KG', 'Kilogram'),
        ('G', 'Gram'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Available quantity")
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='KG', help_text="Unit of measurement")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
