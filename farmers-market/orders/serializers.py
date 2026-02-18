from rest_framework import serializers
from .models import Order, OrderItem, Delivery, DeliveryStatus, DeliveryNotification
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

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ['id', 'status', 'updated_at', 'notes']
        read_only_fields = ['id', 'updated_at']


class DeliverySerializer(serializers.ModelSerializer):
    status_updates = DeliveryStatusSerializer(many=True, read_only=True)
    rider_name = serializers.CharField(source='rider.get_full_name', read_only=True)
    order_details = OrderSerializer(source='order', read_only=True)
    
    class Meta:
        model = Delivery
        fields = ['id', 'order', 'order_details', 'rider', 'rider_name', 'status', 'status_updates',
                  'accepted_at', 'picked_up_at', 'arrived_at', 'completed_at', 'rejection_reason',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'rider', 'rider_name', 'order_details', 'status_updates', 
                            'accepted_at', 'picked_up_at', 'arrived_at', 'completed_at', 'created_at', 'updated_at']


class DeliveryNotificationSerializer(serializers.ModelSerializer):
    delivery_details = DeliverySerializer(source='delivery', read_only=True)
    
    class Meta:
        model = DeliveryNotification
        fields = ['id', 'delivery', 'delivery_details', 'notification_type', 'title', 'message',
                  'is_read', 'created_at', 'read_at']
        read_only_fields = ['id', 'delivery_details', 'created_at', 'read_at']