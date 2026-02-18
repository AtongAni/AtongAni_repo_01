
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import FarmerProfile, CustomerProfile

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "farm_name", "location", "is_approved")
    list_filter = ("is_approved",)

admin.site.register(CustomerProfile)
