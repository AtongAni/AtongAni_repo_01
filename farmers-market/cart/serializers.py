from rest_framework import serializers
from .models import CartItem
from posts.serializers import PostSerializer

class CartItemSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.IntegerField(write_only=True, source='post.id')

    class Meta:
        model = CartItem
        fields = ['id', 'post', 'post_id', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
