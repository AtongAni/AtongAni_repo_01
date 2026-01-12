
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerRegisterSerializer, FarmerRegisterSerializer
from .models import User, FarmerProfile, CustomerProfile
from .permissions import IsNotSuspended
from posts.models import Post
from comments.models import Comment
from orders.models import Order
from django.db.models import Count

class CustomerRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerRegisterSerializer

class FarmerRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FarmerRegisterSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "is_suspended": u.is_suspended,
            "suspension_reason": u.suspension_reason if u.is_suspended else None,
        })


class AdminDashboardView(APIView):
    """Admin dashboard with overview of all activity"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if user is admin
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=403
            )

        # Gather statistics
        total_users = User.objects.count()
        total_farmers = User.objects.filter(role=User.Role.FARMER).count()
        total_customers = User.objects.filter(role=User.Role.CUSTOMER).count()
        total_posts = Post.objects.count()
        total_comments = Comment.objects.count()
        total_orders = Order.objects.count()

        # Recent activity
        recent_users = User.objects.order_by('-date_joined')[:10]
        recent_posts = Post.objects.order_by('-created_at')[:10]
        recent_comments = Comment.objects.order_by('-created_at')[:10]
        recent_orders = Order.objects.order_by('-created_at')[:10]

        return Response({
            'statistics': {
                'total_users': total_users,
                'total_farmers': total_farmers,
                'total_customers': total_customers,
                'total_posts': total_posts,
                'total_comments': total_comments,
                'total_orders': total_orders,
            },
            'recent_activity': {
                'users': [
                    {
                        'id': u.id,
                        'username': u.username,
                        'email': u.email,
                        'role': u.role,
                        'date_joined': u.date_joined,
                    }
                    for u in recent_users
                ],
                'posts': [
                    {
                        'id': p.id,
                        'title': p.title,
                        'author': p.author.username,
                        'created_at': p.created_at,
                    }
                    for p in recent_posts
                ],
                'comments': [
                    {
                        'id': c.id,
                        'content': c.content[:100],
                        'author': c.author.username,
                        'post': c.post.title,
                        'created_at': c.created_at,
                    }
                    for c in recent_comments
                ],
                'orders': [
                    {
                        'id': o.id,
                        'user': o.customer.username,
                        'status': o.status,
                        'total_price': str(sum(item.total_price for item in o.items.all())),
                        'created_at': o.created_at,
                    }
                    for o in recent_orders
                ],
            }
        })


class AllUsersView(APIView):
    """Get all users (admin only)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=403
            )

        users = User.objects.all().values('id', 'username', 'email', 'role', 'date_joined', 'is_active')
        return Response(list(users))


class AllPostsView(APIView):
    """Get all posts with details (admin only)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=403
            )

        posts = Post.objects.annotate(
            comment_count=Count('comments')
        ).values(
            'id', 'title', 'author__username', 'created_at', 'updated_at', 'comment_count'
        )
        return Response(list(posts))


class AllCommentsView(APIView):
    """Get all comments (admin only)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=403
            )

        comments = Comment.objects.values(
            'id', 'content', 'author__username', 'post__title', 'created_at'
        )
        return Response(list(comments))

class UserManagementView(APIView):
    """Get all users with suspension status (admin only)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=403
            )

        users = User.objects.exclude(role=User.Role.ADMIN).values(
            'id', 'username', 'email', 'role', 'is_suspended', 
            'suspended_at', 'suspension_reason', 'date_joined'
        )
        return Response(list(users))


class SuspendUserView(APIView):
    """Suspend a user (admin only)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id=None):
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can perform this action'},
                status=403
            )

        try:
            user = User.objects.get(id=user_id)
            
            # Prevent suspending admin users
            if user.role == User.Role.ADMIN:
                return Response(
                    {'error': 'Cannot suspend admin users'},
                    status=403
                )

            # Prevent suspending yourself
            if user.id == request.user.id:
                return Response(
                    {'error': 'Cannot suspend your own account'},
                    status=403
                )

            reason = request.data.get('reason', 'No reason provided')
            
            from django.utils import timezone
            user.is_suspended = True
            user.suspended_at = timezone.now()
            user.suspension_reason = reason
            user.save()

            return Response({
                'success': f'User {user.username} has been suspended',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_suspended': user.is_suspended,
                    'suspended_at': user.suspended_at,
                    'suspension_reason': user.suspension_reason,
                }
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class ReactivateUserView(APIView):
    """Reactivate a suspended user (admin only)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id=None):
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can perform this action'},
                status=403
            )

        try:
            user = User.objects.get(id=user_id)

            if not user.is_suspended:
                return Response(
                    {'error': 'User is not suspended'},
                    status=400
                )

            user.is_suspended = False
            user.suspended_at = None
            user.suspension_reason = ''
            user.save()

            return Response({
                'success': f'User {user.username} has been reactivated',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_suspended': user.is_suspended,
                }
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)