from rest_framework import serializers
from .models import Post, PostImage, FarmerHarvestProfile
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
        fields = ('id', 'author', 'author_id', 'title', 'content', 'image', 'image_url', 'images', 'price', 'quantity', 'unit', 'post_type', 'created_at', 'updated_at')
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


class FarmerHarvestProfileSerializer(serializers.ModelSerializer):
    farmer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = FarmerHarvestProfile
        fields = (
            'id', 'farmer_name', 'land_size', 'land_size_unit', 
            'crop_type', 'previous_harvest_quantity', 'previous_harvest_unit',
            'previous_harvest_date', 'farming_experience_years', 'location',
            'notes', 'status', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'farmer_name', 'status', 'created_at', 'updated_at')
    
    def get_farmer_name(self, obj):
        return obj.farmer.username
    
    def validate_land_size(self, value):
        if value <= 0:
            raise serializers.ValidationError("Land size must be greater than 0.")
        return value
    
    def validate_crop_type(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Crop type cannot be empty.")
        return value.strip()
    
    def validate(self, data):
        """Validate the entire profile"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication is required.")
        
        # Check if user already has an active profile (only on create)
        if not self.instance:  # Creating new, not updating
            existing_profile = FarmerHarvestProfile.objects.filter(farmer=request.user).first()
            if existing_profile:
                # Allow re-application only if previous was REJECTED or REVISION_REQUESTED
                if existing_profile.status not in ['REJECTED', 'REVISION_REQUESTED']:
                    raise serializers.ValidationError(
                        f"You already have an active harvest forecasting profile with status: {existing_profile.get_status_display()}. "
                        "You can only submit a new application if your previous one was rejected or revision is requested."
                    )
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Request context is required.")
        
        if not request.user.is_authenticated:
            raise serializers.ValidationError("You must be authenticated to create a harvest profile.")
        
        # Set farmer to current user
        validated_data['farmer'] = request.user
        
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create profile: {str(e)}")
    
    def update(self, instance, validated_data):
        # Only allow farmers to update their own profile if it's pending
        request = self.context.get('request')
        if instance.farmer != request.user:
            raise serializers.ValidationError("You can only update your own harvest profile.")
        
        if instance.status != 'PENDING':
            raise serializers.ValidationError("You can only edit a profile that is pending review.")
        
        return super().update(instance, validated_data)
