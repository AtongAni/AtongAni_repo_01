from rest_framework import serializers
from .models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class PostSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    author_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_id', 'title', 'content', 'image', 'price', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_author_id(self, obj):
        """Return the author's ID for frontend ownership checks"""
        return obj.author.id
    
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

