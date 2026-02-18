from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__username', 'id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'post', 'farmer', 'quantity', 'total_price']
    list_filter = ['order__status', 'created_at']
    search_fields = ['post__title', 'farmer__username', 'order__id']
    readonly_fields = ['created_at']
