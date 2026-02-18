from rest_framework import serializers
from .models import Post, PostImage
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'image_url', 'order')
        read_only_fields = ('id',)
    
    def get_image_url(self, obj):
        """Return the full URL for the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class PostSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    author_id = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_id', 'title', 'content', 'image', 'image_url', 'images', 'price', 'quantity', 'unit', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'images')
    
    def get_author_id(self, obj):
        """Return the author's ID for frontend ownership checks"""
        return obj.author.id
    
    def get_image_url(self, obj):
        """Return the full URL for the primary image (first image if available, otherwise legacy image)"""
        # Try to get first image from images relation
        if obj.images.exists():
            first_image = obj.images.first()
            request = self.context.get('request')
            if first_image.image:
                if request:
                    return request.build_absolute_uri(first_image.image.url)
                return first_image.image.url
        
        # Fall back to legacy image field
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        
        return None
    
    def validate_title(self, value):
        """Ensure title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    
    def validate_content(self, value):
        """Ensure content is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value
    
    def validate_image(self, value):
        """Validate image file"""
        if value:
            # Check file size (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file too large (max 5MB).")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Unsupported image format. Allowed: JPEG, PNG, GIF, WebP.")
        
        return value
    
    def create(self, validated_data):
        # Get the user from the request context
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Request context is required to create a post.")

        
        if not request.user.is_authenticated:
            raise serializers.ValidationError("You must be authenticated to create a post.")
        
        # Set author from the request context
        validated_data['author'] = request.user
        return super().create(validated_data)

