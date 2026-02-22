from django.contrib import admin
from django.utils import timezone
from .models import Post, FarmerHarvestProfile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'post_type', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('created_at', 'author__role', 'post_type')


@admin.register(FarmerHarvestProfile)
class FarmerHarvestProfileAdmin(admin.ModelAdmin):
    list_display = ('farmer_name', 'crop_type', 'land_size', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'crop_type')
    search_fields = ('farmer__username', 'farmer__email', 'crop_type', 'location')
    readonly_fields = ('created_at', 'updated_at', 'approved_at')
    
    fieldsets = (
        ('Farmer Information', {
            'fields': ('farmer',)
        }),
        ('Farm Details', {
            'fields': ('land_size', 'land_size_unit', 'crop_type', 'location', 'farming_experience_years', 'notes')
        }),
        ('Previous Harvest', {
            'fields': ('previous_harvest_quantity', 'previous_harvest_unit', 'previous_harvest_date')
        }),
        ('Approval Status', {
            'fields': ('status', 'admin_notes', 'approved_by', 'approved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def farmer_name(self, obj):
        return f"{obj.farmer.username} ({obj.farmer.email})"
    farmer_name.short_description = "Farmer"
    
    def save_model(self, request, obj, form, change):
        # If status changed to APPROVED, set approved_by and approved_at
        if obj.status == 'APPROVED' and not obj.approved_at:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)

