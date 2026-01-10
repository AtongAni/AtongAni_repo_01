from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Post, PostImage
from .serializers import PostSerializer, PostImageSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer
import logging

logger = logging.getLogger(__name__)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_context(self):
        """Ensure request is always in the serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_permissions(self):
        """
        Allow any user to view posts, but only authenticated users can create.
        Only the author can update/delete their own posts.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        try:
            # Let the serializer handle author assignment from context
            # The serializer already sets author in its create() method
            serializer.save()
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}", exc_info=True)
            raise ValidationError(f"Failed to create post: {str(e)}")
    
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own posts.")
        serializer.save()
    
    def perform_destroy(self, instance):
        try:
            if instance.author != self.request.user:
                raise permissions.PermissionDenied("You can only delete your own posts.")
            logger.info(f"Post {instance.id} deleted by user {self.request.user.id}")
            instance.delete()
        except Exception as e:
            logger.error(f"Error deleting post {instance.id}: {str(e)}", exc_info=True)
            raise
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_images(self, request, pk=None):
        """Upload multiple images to a post (max 15)"""
        post = self.get_object()
        
        # Check ownership
        if post.author != request.user:
            return Response({'error': 'You can only add images to your own posts'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get uploaded files
        files = request.FILES.getlist('images')
        
        if not files:
            return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check total image count (max 15)
        current_count = post.images.count()
        if current_count + len(files) > 15:
            return Response(
                {'error': f'Maximum 15 images allowed. You have {current_count}, trying to add {len(files)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_images = []
        errors = []
        
        for idx, file in enumerate(files):
            try:
                # Validate file
                if file.size > 5 * 1024 * 1024:
                    errors.append(f"{file.name}: File too large (max 5MB)")
                    continue
                
                allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
                if file.content_type not in allowed_types:
                    errors.append(f"{file.name}: Unsupported format")
                    continue
                
                # Create PostImage
                post_image = PostImage.objects.create(
                    post=post,
                    image=file,
                    order=current_count + idx
                )
                created_images.append(PostImageSerializer(post_image, context={'request': request}).data)
            except Exception as e:
                errors.append(f"{file.name}: {str(e)}")
        
        return Response({
            'images': created_images,
            'errors': errors if errors else None
        }, status=status.HTTP_201_CREATED if created_images else status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_image(self, request, pk=None):
        """Delete a specific image from a post"""
        post = self.get_object()
        
        # Check ownership
        if post.author != request.user:
            return Response({'error': 'You can only delete images from your own posts'}, status=status.HTTP_403_FORBIDDEN)
        
        image_id = request.data.get('image_id')
        if not image_id:
            return Response({'error': 'image_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            image = PostImage.objects.get(id=image_id, post=post)
            image.delete()
            return Response({'success': 'Image deleted'}, status=status.HTTP_204_NO_CONTENT)
        except PostImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_role(self, request):
        """Filter posts by author role"""
        role = request.query_params.get('role')
        if role:
            posts = Post.objects.filter(author__role=role.upper())
        else:
            posts = Post.objects.all()
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)



class PostCommentViewSet(viewsets.ViewSet):
    """Handle comments nested under posts"""
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, post_id=None):
        """Get all comments for a post"""
        try:
            comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    def retrieve(self, request, post_id=None, pk=None):
        """Get a single comment"""
        try:
            comment = Comment.objects.get(id=pk, post_id=post_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=404)
    
    def create(self, request, post_id=None):
        """Create a new comment on a post"""
        try:
            Post.objects.get(id=post_id)
            data = request.data.copy()
            data['post'] = post_id
            serializer = CommentSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
    
    def partial_update(self, request, post_id=None, pk=None):
        """Update a comment"""
        try:
            comment = Comment.objects.get(id=pk, post_id=post_id)
            if comment.author != request.user:
                return Response({'error': 'You can only edit your own comments'}, status=403)
            
            serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=404)
    
    def destroy(self, request, post_id=None, pk=None):
        """Delete a comment"""
        try:
            comment = Comment.objects.get(id=pk, post_id=post_id)
            if comment.author != request.user:
                return Response({'error': 'You can only delete your own comments'}, status=403)
            
            comment.delete()
            return Response(status=204)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=404)
