# Rider Delivery System Documentation

## Overview
The Rider Delivery System enables delivery personnel to accept, track, and complete orders. Riders receive real-time notifications when orders are ready for delivery and can manage delivery status through a step-by-step tracking system.

## Features

### 1. **Rider Registration**
- New riders can register at `/login` by selecting "Register as rider"
- Required fields:
  - Username
  - Email
  - First & Last Name
  - Phone Number (required)
  - Vehicle Type (optional: motorcycle, car, bicycle, etc.)
  - Vehicle Plate Number (optional)
  - Password

### 2. **Available Deliveries**
- Riders can view all available orders waiting for delivery assignment
- Each delivery shows:
  - Order ID
  - Items included (with quantities)
  - Customer information
  - Total order amount
  - Status badge

### 3. **Accept/Reject Deliveries**
- Riders can accept available deliveries
  - Once accepted, the delivery is assigned to the rider
  - Notification is created in the rider's dashboard
- Riders can reject deliveries with a reason
  - The delivery returns to "PENDING" status
  - Other riders can then accept it

### 4. **Delivery Status Tracking**
Orders progress through the following delivery stages:

```
┌─────────────┐
│  PENDING    │ (Waiting for rider acceptance)
└──────┬──────┘
       │
┌──────▼──────┐
│  ACCEPTED   │ (Rider has accepted the delivery)
└──────┬──────┘
       │
┌──────▼──────────────┐
│ PICKED_UP_OTW       │ (Rider is on the way to pickup location)
└──────┬──────────────┘
       │
┌──────▼──────┐
│ PICKED_UP   │ (Items have been picked up)
└──────┬──────┘
       │
┌──────▼──────────────┐
│ OTW_TO_BUYER        │ (Rider is on the way to buyer)
└──────┬──────────────┘
       │
┌──────▼──────┐
│  ARRIVED    │ (Rider arrived at buyer's location)
└──────┬──────┘
       │
┌──────▼──────┐
│ COMPLETED   │ (Delivery successfully completed)
└─────────────┘
```

### 5. **Real-time Status Updates**
- Riders can update delivery status with optional notes
- Each update is timestamped and logged
- Customers can track delivery progress in real-time
- Status history is maintained for audit purposes

### 6. **Delivery Notifications**
- Riders receive instant notifications when:
  - **NEW_DELIVERY**: New order is available for pickup
  - **DELIVERY_EXPIRED**: A delivery was rejected (can be picked up again)
  - **STATUS_UPDATE**: Delivery status has been updated
- Notifications can be marked as read
- Unread notifications show a visual indicator

### 7. **Rider Dashboard**
Access via Dashboard → Deliveries tab

#### Available Deliveries Tab
- Browse all unassigned deliveries
- Quick accept/reject buttons
- Filter and sort options

#### Active Deliveries Tab
- View current assignments
- Update delivery status with real-time tracker
- Mark delivery as complete when arrived
- View delivery history

#### Notifications Tab
- View all notifications
- Filter by type (New, Expired, Updates)
- Mark notifications as read
- Clear old notifications

## API Endpoints

### Delivery Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/deliveries/available/` | List unassigned deliveries |
| GET | `/api/deliveries/my_deliveries/` | List all rider's deliveries |
| GET | `/api/deliveries/my_pending/` | List active deliveries |
| POST | `/api/deliveries/{id}/accept/` | Accept a delivery |
| POST | `/api/deliveries/{id}/reject/` | Reject a delivery |
| POST | `/api/deliveries/{id}/update_status/` | Update delivery status |
| POST | `/api/deliveries/{id}/complete/` | Mark delivery complete |

### Notification Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/my_notifications/` | Get all notifications |
| GET | `/api/notifications/unread/` | Get unread notifications |
| PATCH | `/api/notifications/{id}/mark_as_read/` | Mark as read |

## Database Models

### RiderProfile
```python
- user: OneToOneField (User)
- phone: CharField
- vehicle_type: CharField
- vehicle_plate: CharField
- is_verified: BooleanField
- rating: DecimalField (3.2 format)
- total_deliveries: IntegerField
```

### Delivery
```python
- order: OneToOneField (Order)
- rider: ForeignKey (User) - nullable
- status: CharField (choices above)
- created_at: DateTimeField
- updated_at: DateTimeField
- accepted_at: DateTimeField (nullable)
- picked_up_at: DateTimeField (nullable)
- arrived_at: DateTimeField (nullable)
- completed_at: DateTimeField (nullable)
- rejection_reason: TextField
```

### DeliveryStatus
```python
- delivery: ForeignKey (Delivery)
- status: CharField
- updated_at: DateTimeField
- notes: TextField
```

### DeliveryNotification
```python
- delivery: ForeignKey (Delivery)
- rider: ForeignKey (User)
- notification_type: CharField
- title: CharField
- message: TextField
- is_read: BooleanField
- created_at: DateTimeField
- read_at: DateTimeField (nullable)
```

## Frontend Components

### RiderDashboard.jsx
- Main dashboard component
- Tab navigation (Available, Active, Notifications)
- Handles all rider-related operations

### DeliveryCard.jsx
- Individual delivery display
- Accept/Reject functionality
- Status update form

### DeliveryStatusTracker.jsx
- Visual progress indicator
- Shows delivery steps completed
- Displays status history

### RiderNotifications.jsx
- Notifications list
- Mark as read functionality
- Notification type indicators

## Usage Example

### For Riders:

1. **Register**
   ```
   Navigate to /login → "Register as rider"
   Fill in registration form with vehicle details
   ```

2. **Accept Delivery**
   ```
   Dashboard → Deliveries → Available Deliveries
   Click "Accept Delivery" on any available order
   ```

3. **Update Status**
   ```
   Dashboard → Deliveries → Active Deliveries
   Click "Update Delivery Status"
   Select: On the Way to Pickup → Picked Up → On the Way to Buyer → Arrived
   ```

4. **Complete Delivery**
   ```
   After "Arrived" status reached
   Click "Mark Delivery as Complete"
   Delivery tracked as completed
   ```

### For Farmers:

After approving an order:
- A Delivery record is automatically created
- All verified riders receive notifications
- Farmer can see delivery status in real-time
- Once completed, order shows as delivered

### For Customers:

When order is approved:
- Delivery tracking becomes available
- Can see rider's current status
- Receive notifications of delivery progress
- Can confirm receipt once rider arrives

## Integration with Order System

When order status becomes "APPROVED":
1. **Delivery Created**: New Delivery record created with status "PENDING"
2. **Notifications Sent**: All verified riders receive notification
3. **Status Updates**: Farmers can track delivery progress
4. **Completion**: When rider completes, order status updates to "COMPLETED"

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Delivery already accepted | Another rider accepted first | Try another available delivery |
| Invalid status transition | Status progression violated | Follow correct order of steps |
| Unauthorized | Not assigned to this delivery | Only riders can update their deliveries |
| Unverified rider | Rider account not verified | Complete verification process (future feature) |

## Future Enhancements

1. **Rider Ratings & Reviews**
   - Customers rate riders after delivery
   - Display rating in rider profile
   - Track performance metrics

2. **GPS Tracking**
   - Real-time location tracking
   - Route optimization
   - ETA calculation

3. **Payment Integration**
   - Automatic payment for completed deliveries
   - Earnings dashboard
   - Withdrawal management

4. **Document Verification**
   - ID verification
   - License verification
   - Background check status

5. **Performance Analytics**
   - Delivery success rate
   - Average delivery time
   - Customer satisfaction score

6. **Push Notifications**
   - Real-time delivery notifications
   - Status update alerts
   - Earnings notifications

## Testing

### Test Scenarios

1. **Rider Registration**
   - Register with valid data ✓
   - Reject duplicate username ✓
   - Validate phone number format

2. **Accept Delivery**
   - View available deliveries ✓
   - Accept delivery ✓
   - Prevent duplicate acceptance ✓

3. **Status Updates**
   - Update through all steps ✓
   - Log each update with timestamp ✓
   - Prevent backward status changes

4. **Notifications**
   - Create notification on new delivery ✓
   - Mark as read ✓
   - List by type ✓

## API Usage Examples

### Accept a Delivery
```bash
POST /api/deliveries/5/accept/
Content-Type: application/json
Authorization: Bearer {token}

Response:
{
  "message": "Delivery accepted successfully",
  "delivery": {
    "id": 5,
    "order": 10,
    "rider": "john_rider",
    "status": "ACCEPTED",
    "accepted_at": "2024-02-13T10:30:00Z"
  }
}
```

### Update Delivery Status
```bash
POST /api/deliveries/5/update_status/
Content-Type: application/json
Authorization: Bearer {token}

{
  "status": "PICKED_UP",
  "notes": "Package picked up, heading to buyer location"
}

Response:
{
  "message": "Delivery status updated to PICKED_UP",
  "delivery": {
    "id": 5,
    "status": "PICKED_UP",
    "picked_up_at": "2024-02-13T10:45:00Z"
  }
}
```

### Get Unread Notifications
```bash
GET /api/notifications/unread/
Authorization: Bearer {token}

Response:
[
  {
    "id": 1,
    "notification_type": "NEW_DELIVERY",
    "title": "New Delivery Available",
    "message": "Order #10 is ready for delivery",
    "is_read": false
  }
]
```

## Configuration

### Environment Variables
None specific to rider system (uses existing Django settings)

### Django Settings
Already configured in `settings.py`:
- Rider role added to User.Role choices
- Orders app includes new riders imports
- CORS configured for frontend access

## Troubleshooting

### Riders not seeing available deliveries
- Check if rider is verified (future feature)
- Ensure order status is "APPROVED"
- Check notification permissions

### Status update fails
- Verify correct status progression
- Check correct delivery assignment
- Verify authentication token valid

### Delivery not displaying
- Check if order exists and is approved
- Verify delivery record created
- Check user role (must be RIDER)

## Support

For issues or questions:
1. Check error message details
2. Verify authentication token
3. Check database migrations applied
4. Review API endpoint documentation
5. Contact development team

---

**Version**: 1.0.0  
**Last Updated**: February 13, 2026  
**Maintained By**: Development Team
