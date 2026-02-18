from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1, help_text="Quantity ordered")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s cart - {self.post.title} ({self.quantity} {self.post.unit})"
