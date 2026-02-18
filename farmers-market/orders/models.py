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

class Delivery(models.Model):
    """Represents a delivery assignment for an order"""
    DELIVERY_STATUS_CHOICES = [
        ('PENDING', 'Pending - Awaiting Rider'),
        ('ACCEPTED', 'Accepted by Rider'),
        ('PICKED_UP_OTW', 'On the Way to Pickup'),
        ('PICKED_UP', 'Picked Up'),
        ('OTW_TO_BUYER', 'On the Way to Buyer'),
        ('ARRIVED', 'Arrived at Buyer'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected by Rider'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    rider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries', limit_choices_to={'role': 'RIDER'})
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, help_text="Reason for rejection if rider rejects")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Delivery #{self.id} - Order #{self.order.id} ({self.status})"


class DeliveryStatus(models.Model):
    """Tracks individual delivery status updates"""
    STATUS_CHOICES = [
        ('PICKED_UP_OTW', 'On the Way to Pickup'),
        ('PICKED_UP', 'Picked Up'),
        ('OTW_TO_BUYER', 'On the Way to Buyer'),
        ('ARRIVED', 'Arrived at Buyer'),
    ]
    
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Delivery #{self.delivery.id} - {self.status} at {self.updated_at}"


class DeliveryNotification(models.Model):
    """Notifies riders about new deliveries"""
    NOTIFICATION_TYPES = [
        ('NEW_DELIVERY', 'New Delivery Available'),
        ('DELIVERY_EXPIRED', 'Delivery Offer Expired'),
        ('STATUS_UPDATE', 'Delivery Status Update'),
    ]
    
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='notifications')
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_notifications', limit_choices_to={'role': 'RIDER'})
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.rider.username} - {self.notification_type}"