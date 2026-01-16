from rest_framework import serializers
from .models import Order, OrderItem
from posts.serializers import PostSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.IntegerField(write_only=True, source='post.id', required=False)
    farmer_name = serializers.CharField(source='farmer.username', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'post', 'post_id', 'farmer_name', 'quantity', 'price', 'total_price', 'unit', 'created_at']
        read_only_fields = ['id', 'farmer_name', 'total_price', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'status', 'items', 'total_amount', 'rejection_reason', 
                  'approved_at', 'delivery_confirmation_shown_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'customer_name', 'approved_at', 'delivery_confirmation_shown_at', 'created_at', 'updated_at']
    
    def get_total_amount(self, obj):
        return sum(item.total_price for item in obj.items.all())


class OrderDetailSerializer(OrderSerializer):
    """Detailed order serializer with all information"""
    pass
