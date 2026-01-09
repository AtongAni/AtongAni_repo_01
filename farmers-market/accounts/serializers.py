
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import FarmerProfile, CustomerProfile

User = get_user_model()


class BaseRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    access = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name", "access")

    def create_user(self, role, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=role,
        )
        return user

    def get_access(self, obj):
        """Generate JWT access token after user creation"""
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)


class CustomerRegisterSerializer(BaseRegisterSerializer):
    phone = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta(BaseRegisterSerializer.Meta):
        fields = BaseRegisterSerializer.Meta.fields + ("phone",)

    def create(self, validated_data):
        phone = validated_data.pop("phone", "")
        user = self.create_user(role=User.Role.CUSTOMER, validated_data=validated_data)
        CustomerProfile.objects.create(user=user, phone=phone)
        return user


class FarmerRegisterSerializer(BaseRegisterSerializer):
    farm_name = serializers.CharField(write_only=True, required=True)
    location = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta(BaseRegisterSerializer.Meta):
        fields = BaseRegisterSerializer.Meta.fields + ("farm_name", "location")

    def create(self, validated_data):
        farm_name = validated_data.pop("farm_name")
        location = validated_data.pop("location", "")
        user = self.create_user(role=User.Role.FARMER, validated_data=validated_data)
        FarmerProfile.objects.create(user=user, farm_name=farm_name, location=location)
        return user
       
