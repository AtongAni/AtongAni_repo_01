from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('APPROVED', 'Approved'),
        ('SIMULATION_DELIVERY', 'Simulation Delivery'),  # 10-second middle event before customer confirmation
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True, help_text="Timestamp when farmer approved the order")
    delivery_confirmation_shown_at = models.DateTimeField(blank=True, null=True, help_text="Timestamp when simulation delivery began")
    rejection_reason = models.TextField(blank=True, null=True, help_text="Reason for rejection if applicable")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name='order_items')
    farmer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_orders')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unit = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"OrderItem - {self.post.title} x {self.quantity} ({self.order.status})"
