from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import Delivery, DeliveryNotification, DeliveryStatus, Order
from .serializers import DeliverySerializer, DeliveryNotificationSerializer
from accounts.models import User


class IsRider:
    """Check if user is a rider"""
    def has_permission(self, request):
        return request.user.is_authenticated and request.user.role == 'RIDER'


class DeliveryViewSet(viewsets.ModelViewSet):
    """ViewSet for rider delivery management"""
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    
    def get_queryset(self):
        user = self.request.user
        # Riders see deliveries assigned to them
        if user.role == 'RIDER':
            return Delivery.objects.filter(rider=user)
        # Admins/staff can see all
        if user.is_staff:
            return Delivery.objects.all()
        # Others can't see deliveries
        return Delivery.objects.none()
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available deliveries (not yet assigned to a rider)"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can view available deliveries'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get all pending deliveries not assigned to anyone
        available_deliveries = Delivery.objects.filter(
            status='PENDING',
            rider__isnull=True
        )
        
        serializer = self.get_serializer(available_deliveries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def accept(self, request, pk=None):
        """Rider accepts a delivery"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can accept deliveries'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        delivery = self.get_object()
        
        if delivery.status != 'PENDING':
            return Response(
                {'error': f'Cannot accept delivery with status: {delivery.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if delivery.rider is not None and delivery.rider != request.user:
            return Response(
                {'error': 'This delivery has already been accepted by another rider'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        delivery.rider = request.user
        delivery.status = 'ACCEPTED'
        delivery.accepted_at = timezone.now()
        delivery.save()
        
        # Create notification for the rider
        DeliveryNotification.objects.create(
            delivery=delivery,
            rider=request.user,
            notification_type='NEW_DELIVERY',
            title='Delivery Accepted',
            message=f'You have accepted delivery for Order #{delivery.order.id}'
        )
        
        serializer = self.get_serializer(delivery)
        return Response(
            {
                'message': 'Delivery accepted successfully',
                'delivery': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def reject(self, request, pk=None):
        """Rider rejects a delivery"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can reject deliveries'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        delivery = self.get_object()
        
        if delivery.status != 'PENDING' and delivery.status != 'ACCEPTED':
            return Response(
                {'error': f'Cannot reject delivery with status: {delivery.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if delivery.rider != request.user:
            return Response(
                {'error': 'You are not authorized to reject this delivery'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        rejection_reason = request.data.get('reason', 'No reason provided')
        delivery.status = 'REJECTED'
        delivery.rejection_reason = rejection_reason
        delivery.rider = None
        delivery.save()
        
        # Create notification about rejection
        DeliveryNotification.objects.create(
            delivery=delivery,
            rider=request.user,
            notification_type='DELIVERY_EXPIRED',
            title='Delivery Rejected',
            message=f'You have rejected delivery for Order #{delivery.order.id}'
        )
        
        serializer = self.get_serializer(delivery)
        return Response(
            {
                'message': 'Delivery rejected successfully',
                'delivery': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def update_status(self, request, pk=None):
        """Update delivery status through steps: picked_up_otw -> picked_up -> otw_to_buyer -> arrived"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can update delivery status'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        delivery = self.get_object()
        
        if delivery.rider != request.user:
            return Response(
                {'error': 'You are not authorized to update this delivery'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        
        if new_status not in ['PICKED_UP_OTW', 'PICKED_UP', 'OTW_TO_BUYER', 'ARRIVED']:
            return Response(
                {'error': f'Invalid status: {new_status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate status progression
        status_order = ['PICKED_UP_OTW', 'PICKED_UP', 'OTW_TO_BUYER', 'ARRIVED']
        if delivery.status not in ['ACCEPTED'] and new_status not in status_order:
            return Response(
                {'error': 'Invalid status transition'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update delivery status
        delivery.status = new_status
        
        # Track timestamps
        if new_status == 'PICKED_UP':
            delivery.picked_up_at = timezone.now()
        elif new_status == 'ARRIVED':
            delivery.arrived_at = timezone.now()
        
        delivery.save()
        
        # Create status update record
        DeliveryStatus.objects.create(
            delivery=delivery,
            status=new_status,
            notes=request.data.get('notes', '')
        )
        
        # Create notification
        status_labels = {
            'PICKED_UP_OTW': 'On the way to pick up',
            'PICKED_UP': 'Picked up from sender',
            'OTW_TO_BUYER': 'On the way to buyer',
            'ARRIVED': 'Arrived at buyer location'
        }
        
        DeliveryNotification.objects.create(
            delivery=delivery,
            rider=request.user,
            notification_type='STATUS_UPDATE',
            title='Delivery Status Updated',
            message=f'Delivery status: {status_labels.get(new_status, new_status)}'
        )
        
        serializer = self.get_serializer(delivery)
        return Response(
            {
                'message': f'Delivery status updated to {new_status}',
                'delivery': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def complete(self, request, pk=None):
        """Rider marks delivery as complete (only after ARRIVED status)"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can complete deliveries'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        delivery = self.get_object()
        
        if delivery.rider != request.user:
            return Response(
                {'error': 'You are not authorized to complete this delivery'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if delivery.status != 'ARRIVED':
            return Response(
                {'error': f'Delivery must be in ARRIVED status to complete. Current: {delivery.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        delivery.status = 'COMPLETED'
        delivery.completed_at = timezone.now()
        delivery.save()
        
        # Update order status to COMPLETED
        delivery.order.status = 'COMPLETED'
        delivery.order.save()
        
        # Update rider's delivery count
        if hasattr(request.user, 'rider_profile'):
            request.user.rider_profile.total_deliveries += 1
            request.user.rider_profile.save()
        
        serializer = self.get_serializer(delivery)
        return Response(
            {
                'message': 'Delivery completed successfully',
                'delivery': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def my_deliveries(self, request):
        """Get all rider's deliveries (completed and active)"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can view deliveries'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        deliveries = Delivery.objects.filter(rider=request.user).order_by('-created_at')
        serializer = self.get_serializer(deliveries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_pending(self, request):
        """Get rider's pending/active deliveries"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can view deliveries'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        pending_statuses = ['ACCEPTED', 'PICKED_UP_OTW', 'PICKED_UP', 'OTW_TO_BUYER', 'ARRIVED']
        deliveries = Delivery.objects.filter(
            rider=request.user,
            status__in=pending_statuses
        ).order_by('-updated_at')
        
        serializer = self.get_serializer(deliveries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryNotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for rider delivery notifications"""
    serializer_class = DeliveryNotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']
    
    def get_queryset(self):
        user = self.request.user
        # Riders see their own notifications
        if user.role == 'RIDER':
            return DeliveryNotification.objects.filter(rider=user).order_by('-created_at')
        # Admins/staff can see all
        if user.is_staff:
            return DeliveryNotification.objects.all()
        # Others can't see notifications
        return DeliveryNotification.objects.none()
    
    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        
        if notification.rider != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You are not authorized to mark this notification'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications for the rider"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can view notifications'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        unread_notifications = DeliveryNotification.objects.filter(
            rider=request.user,
            is_read=False
        ).order_by('-created_at')
        
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        """Get all notifications for the rider"""
        if request.user.role != 'RIDER':
            return Response(
                {'error': 'Only riders can view notifications'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notifications = DeliveryNotification.objects.filter(
            rider=request.user
        ).order_by('-created_at')
        
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
