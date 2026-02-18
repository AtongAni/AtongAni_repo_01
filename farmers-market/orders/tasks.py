"""
Orders tasks - Handles asynchronous operations for orders

Simulation Delivery: A 10-second middle event that represents delivery in progress.
This is a placeholder for future real delivery integration (e.g., GPS tracking, 
third-party delivery APIs, etc.). When ready to implement real delivery, 
replace this simulation with actual delivery logic.
"""
import time
from django.utils import timezone
from .models import Order


def trigger_simulation_delivery(order_id):
    """
    Triggers simulation delivery after 10 seconds of order approval.
    
    This function:
    1. Waits 10 seconds (simulating delivery time)
    2. Updates order status to SIMULATION_DELIVERY
    3. Marks delivery_confirmation_shown_at timestamp
    
    When implementing real delivery:
    - Replace sleep with actual delivery logic (API calls, tracking, etc.)
    - Keep the status update and timestamp recording
    - Maintain the database state for customer confirmation flow
    
    Args:
        order_id: The ID of the order to transition to delivery
    """
    # Simulate delivery taking 10 seconds
    time.sleep(10)
    
    try:
        order = Order.objects.get(id=order_id)
        
        # Only update if order is still in APPROVED state
        if order.status == 'APPROVED':
            order.status = 'SIMULATION_DELIVERY'
            order.delivery_confirmation_shown_at = timezone.now()
            order.save(update_fields=['status', 'delivery_confirmation_shown_at', 'updated_at'])
    except Order.DoesNotExist:
        pass
