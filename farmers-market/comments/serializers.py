from rest_framework import serializers
from .models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'post')
    
    def create(self, validated_data):
        validated_data.pop('author_id', None)
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
