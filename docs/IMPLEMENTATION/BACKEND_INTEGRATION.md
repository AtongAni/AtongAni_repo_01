# Backend Integration Guide

This guide explains what backend endpoints and models are needed to support the new dashboard features.

## Models Required

### 1. Post Model
```python
class Post(models.Model):
    author = ForeignKey(User, on_delete=models.CASCADE)
    title = CharField(max_length=100)
    content = TextField()
    price = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### 2. Comment Model
```python
class Comment(models.Model):
    post = ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = ForeignKey(User, on_delete=models.CASCADE)
    text = TextField(max_length=500)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### 3. CartItem Model
```python
class CartItem(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    post = ForeignKey(Post, on_delete=models.CASCADE)
    quantity = PositiveIntegerField(default=1)
    added_at = DateTimeField(auto_now_add=True)
```

### 4. Order Model (for checkout)
```python
class Order(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    created_at = DateTimeField(auto_now_add=True)
```

## API Endpoints Required

### Posts Endpoints
```
GET  /api/posts/                    - List posts (filter by role optional)
POST /api/posts/                    - Create post (farmer only)
GET  /api/posts/{id}/               - Get post details
PATCH /api/posts/{id}/              - Update post (owner only)
DELETE /api/posts/{id}/             - Delete post (owner only)
```

### Comments Endpoints
```
GET  /api/posts/{postId}/comments/            - List comments
POST /api/posts/{postId}/comments/            - Create comment (auth required)
PATCH /api/posts/{postId}/comments/{id}/      - Update comment (owner only)
DELETE /api/posts/{postId}/comments/{id}/     - Delete comment (owner only)
```

### Cart Endpoints
```
GET  /api/cart/                     - Get user's cart items
POST /api/cart/                     - Add item to cart (customer only)
PATCH /api/cart/{id}/               - Update quantity (owner only)
DELETE /api/cart/{id}/              - Remove item (owner only)
POST /api/cart/checkout/            - Checkout and create order
```

## Serializers Example (Django REST Framework)

```python
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'author_id', 'title', 'content', 'price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'author_id', 'text', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='post.title', read_only=True)
    price = serializers.DecimalField(source='post.price', max_digits=10, decimal_places=2, read_only=True)
    farmer_name = serializers.CharField(source='post.author.username', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'post', 'title', 'price', 'farmer_name', 'quantity']
```

## ViewSets Example (Django REST Framework)

```python
from rest_framework import viewsets, permissions

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart_items = self.get_queryset()
        total = sum(item.post.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total)
        cart_items.delete()
        return Response({'order_id': order.id})
```

## URL Configuration

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, CartViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/posts/<int:post_id>/comments/<int:pk>/', CommentViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
]
```

## Frontend API Calls

All frontend API calls are in these files:
- `src/api/posts.js` - Post operations
- `src/api/comments.js` - Comment operations
- `src/api/cart.js` - Cart operations

These files make HTTP requests to the backend endpoints defined above.

## Important Notes

1. **Authentication:** All endpoints except login/register require valid JWT token
2. **Permissions:** Only allow farmers to create posts, only customers to use cart
3. **Filtering:** Frontend sends `?role=farmer` to filter posts by farmer
4. **CORS:** Configure CORS to allow requests from frontend domain
5. **Pagination:** Consider adding pagination for large post lists
6. **Image Uploads:** For post images, implement separate image upload endpoints
