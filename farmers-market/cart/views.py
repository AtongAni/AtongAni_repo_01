from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CartItem
from .serializers import CartItemSerializer
from posts.models import Post

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Add item to cart or update quantity if already exists"""
        post_id = request.data.get('post')
        quantity = request.data.get('quantity', 1)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent farmers from adding their own products to cart
        if post.author == request.user:
            return Response(
                {'error': 'You cannot add your own products to cart'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate quantity doesn't exceed available stock
        try:
            quantity_decimal = float(quantity)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid quantity format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity_decimal <= 0:
            return Response(
                {'error': 'Quantity must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity_decimal > float(post.quantity):
            return Response(
                {'error': f'Quantity exceeds available stock. Available: {post.quantity} {post.unit}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'quantity': quantity_decimal}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity_decimal
            if new_quantity > float(post.quantity):
                return Response(
                    {'error': f'Total quantity exceeds available stock. Available: {post.quantity} {post.unit}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update cart item quantity"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Checkout cart - reduce post quantities, delete sold-out posts, and clear cart items"""
        cart_items = CartItem.objects.filter(user=request.user)
        count = cart_items.count()
        
        if count == 0:
            return Response(
                {'message': 'Cart is already empty'},
                status=status.HTTP_200_OK
            )
        
        # Process each cart item
        deleted_posts = []
        for cart_item in cart_items:
            post = cart_item.post
            # Reduce post quantity by the amount purchased
            post.quantity -= cart_item.quantity
            
            # If quantity reaches zero or below, delete the post
            if post.quantity <= 0:
                deleted_posts.append(post.title)
                post.delete()
            else:
                post.save()
        
        # Clear all cart items for this user
        cart_items.delete()
        
        response_msg = f'Checked out {count} items'
        if deleted_posts:
            response_msg += f'. Sold-out posts deleted: {", ".join(deleted_posts)}'
        
        return Response(
            {'message': response_msg, 'deleted_posts': deleted_posts},
            status=status.HTTP_200_OK
        )
