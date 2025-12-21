
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FarmerProfile, CustomerProfile

User = get_user_model()


class BaseRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create_user(self, role, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            role=role,
        )
        return user


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
    farm_name = serializers.CharField(write_only=True)
    location = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta(BaseRegisterSerializer.Meta):
        fields = BaseRegisterSerializer.Meta.fields + ("farm_name", "location")

    def create(self, validated_data):
        farm_name = validated_data.pop("farm_name")
        location = validated_data.pop("location", "")
        user = self.create_user(role=User.Role.FARMER, validated_data=validated_data)
        FarmerProfile.objects.create(user=user, farm_name=farm_name, location=location)
        return user
       
