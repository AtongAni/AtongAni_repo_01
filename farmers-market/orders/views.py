from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
import threading
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderDetailSerializer
from .tasks import trigger_simulation_delivery
from cart.models import CartItem
from posts.models import Post

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        # Customers see their own orders
        # Farmers see orders for their products
        if hasattr(user, 'farmer_profile'):
            # Farmer can see all orders for their products
            return Order.objects.filter(items__farmer=user).distinct()
        else:
            # Customer sees their own orders
            return Order.objects.filter(customer=user)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def checkout(self, request):
        """Create order from cart items - sets status to IN_PROGRESS"""
        cart_items = CartItem.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create order with IN_PROGRESS status
        order = Order.objects.create(
            customer=request.user,
            status='IN_PROGRESS'
        )
        
        # Create order items from cart items
        for cart_item in cart_items:
            post = cart_item.post
            OrderItem.objects.create(
                order=order,
                post=post,
                farmer=post.author,
                quantity=cart_item.quantity,
                price=post.price,
                unit=post.unit
            )
        
        # Don't clear cart yet - customer can still see their order status
        serializer = self.get_serializer(order)
        return Response(
            {
                'message': 'Order created and awaiting farmer approval',
                'order': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve(self, request, pk=None):
        """Farmer approves an order"""
        order = self.get_object()
        
        # Check if user is the farmer for at least one item in this order
        user_order_items = order.items.filter(farmer=request.user)
        if not user_order_items.exists():
            return Response(
                {'error': 'You are not authorized to approve this order'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if order.status != 'IN_PROGRESS':
            return Response(
                {'error': f'Cannot approve order with status: {order.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Process each order item from this farmer
        for order_item in user_order_items:
            post = order_item.post
            # Reduce post quantity
            if post.quantity >= order_item.quantity:
                post.quantity -= order_item.quantity
                if post.quantity <= 0:
                    post.delete()
                else:
                    post.save()
            else:
                return Response(
                    {'error': f'Insufficient stock for {post.title}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # If all items from all farmers are processed, mark order as APPROVED
        order.status = 'APPROVED'
        order.approved_at = timezone.now()
        order.save()
        
        # Clear cart for this order's customer
        CartItem.objects.filter(user=order.customer).delete()
        
        # Trigger simulation delivery after 10 seconds (in background thread)
        # This will update order status to SIMULATION_DELIVERY after 10 seconds
        delivery_thread = threading.Thread(
            target=trigger_simulation_delivery,
            args=(order.id,),
            daemon=True
        )
        delivery_thread.start()
        
        serializer = self.get_serializer(order)
        return Response(
            {
                'message': 'Order approved successfully',
                'order': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def reject(self, request, pk=None):
        """Farmer rejects an order - items return to customer's cart"""
        order = self.get_object()
        
        # Check if user is the farmer for at least one item in this order
        user_order_items = order.items.filter(farmer=request.user)
        if not user_order_items.exists():
            return Response(
                {'error': 'You are not authorized to reject this order'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if order.status != 'IN_PROGRESS':
            return Response(
                {'error': f'Cannot reject order with status: {order.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rejection_reason = request.data.get('reason', 'No reason provided')
        order.rejection_reason = rejection_reason
        order.status = 'REJECTED'
        order.save()
        
        # Return items to customer's cart
        for order_item in order.items.all():
            CartItem.objects.update_or_create(
                user=order.customer,
                post=order_item.post,
                defaults={'quantity': order_item.quantity}
            )
        
        serializer = self.get_serializer(order)
        return Response(
            {
                'message': 'Order rejected. Items returned to your cart',
                'order': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def my_pending_orders(self, request):
        """Get orders awaiting this farmer's approval"""
        if not hasattr(request.user, 'farmer_profile'):
            return Response(
                {'error': 'Only farmers can view pending orders'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        pending_orders = Order.objects.filter(
            items__farmer=request.user,
            status='IN_PROGRESS'
        ).distinct()
        
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Get customer's orders with all statuses"""
        orders = Order.objects.filter(customer=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'])
    def confirm_received(self, request, pk=None):
        """
        Customer confirms they have received their order.
        
        This endpoint transitions order from SIMULATION_DELIVERY to COMPLETED.
        When real delivery is implemented, this endpoint will verify delivery
        completion (e.g., check GPS location, delivery signature, etc.)
        and then mark the order as COMPLETED.
        
        Args:
            pk: Order ID
            
        Returns:
            Updated order with COMPLETED status
        """
        order = self.get_object()
        
        # Verify this is the customer who placed the order
        if order.customer != request.user:
            return Response(
                {'error': 'You are not authorized to confirm this order'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Can only confirm if order is in SIMULATION_DELIVERY status
        if order.status != 'SIMULATION_DELIVERY':
            return Response(
                {'error': f'Cannot confirm order with status: {order.status}. '
                          f'Order must be in delivery status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark order as COMPLETED
        order.status = 'COMPLETED'
        order.save(update_fields=['status', 'updated_at'])
        
        serializer = self.get_serializer(order)
        return Response(
            {
                'message': 'Order confirmed as received',
                'order': serializer.data
            },
            status=status.HTTP_200_OK
        )