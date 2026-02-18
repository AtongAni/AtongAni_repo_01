# Rider API Quick Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints (except login/register) require JWT token:
```
Authorization: Bearer {your_access_token}
```

---

## Registration

### Register as Rider
```bash
POST /auth/register/rider/

Body:
{
  "username": "john_rider",
  "email": "john@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "vehicle_type": "motorcycle",
  "vehicle_plate": "ABC-1234"
}

Response (201):
{
  "id": 5,
  "username": "john_rider",
  "email": "john@example.com",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Deliveries

### List Available Deliveries
```bash
GET /deliveries/available/

Query Parameters:
- (none currently)

Response (200):
[
  {
    "id": 1,
    "order": 10,
    "rider": null,
    "status": "PENDING",
    "order_details": { ... },
    "created_at": "2024-02-13T10:00:00Z"
  }
]
```

### List My Deliveries
```bash
GET /deliveries/my_deliveries/

Response (200):
[
  {
    "id": 1,
    "order": 10,
    "rider": "john_rider",
    "status": "COMPLETED",
    "completed_at": "2024-02-13T14:00:00Z"
  }
]
```

### List My Pending Deliveries
```bash
GET /deliveries/my_pending/

Response (200):
[
  {
    "id": 2,
    "order": 11,
    "status": "OTW_TO_BUYER"
  }
]
```

### Accept Delivery
```bash
POST /deliveries/{id}/accept/

Body: {} (empty)

Response (200):
{
  "message": "Delivery accepted successfully",
  "delivery": {
    "id": 1,
    "status": "ACCEPTED",
    "accepted_at": "2024-02-13T10:30:00Z"
  }
}

Errors:
- 403: Not a rider or already rejected/accepted
- 400: Invalid delivery status
```

### Reject Delivery
```bash
POST /deliveries/{id}/reject/

Body:
{
  "reason": "Vehicle is broken down"
}

Response (200):
{
  "message": "Delivery rejected successfully",
  "delivery": {
    "id": 1,
    "status": "REJECTED",
    "rejection_reason": "Vehicle is broken down"
  }
}
```

### Update Delivery Status
```bash
POST /deliveries/{id}/update_status/

Body:
{
  "status": "PICKED_UP",
  "notes": "Items picked up, heading to buyer"
}

Valid Statuses:
- PICKED_UP_OTW
- PICKED_UP
- OTW_TO_BUYER
- ARRIVED

Response (200):
{
  "message": "Delivery status updated to PICKED_UP",
  "delivery": {
    "id": 1,
    "status": "PICKED_UP",
    "status_updates": [
      {
        "status": "PICKED_UP",
        "updated_at": "2024-02-13T10:45:00Z",
        "notes": "Items picked up, heading to buyer"
      }
    ]
  }
}
```

### Complete Delivery
```bash
POST /deliveries/{id}/complete/

Body: {} (empty)

Prerequisites:
- Delivery status must be ARRIVED

Response (200):
{
  "message": "Delivery completed successfully",
  "delivery": {
    "id": 1,
    "status": "COMPLETED",
    "completed_at": "2024-02-13T14:00:00Z"
  }
}

Errors:
- 400: Delivery not in ARRIVED status
- 403: Unauthorized
```

---

## Notifications

### List My Notifications
```bash
GET /notifications/my_notifications/

Response (200):
[
  {
    "id": 1,
    "delivery": 10,
    "notification_type": "NEW_DELIVERY",
    "title": "New Delivery Available",
    "message": "Order #10 is ready for delivery",
    "is_read": false,
    "created_at": "2024-02-13T10:00:00Z"
  },
  {
    "id": 2,
    "delivery": 10,
    "notification_type": "STATUS_UPDATE",
    "title": "Delivery Status Updated",
    "message": "Order #10: On the way to buyer",
    "is_read": true,
    "created_at": "2024-02-13T11:00:00Z",
    "read_at": "2024-02-13T11:05:00Z"
  }
]
```

### List Unread Notifications
```bash
GET /notifications/unread/

Response (200):
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

### Mark Notification as Read
```bash
PATCH /notifications/{id}/mark_as_read/

Body: {} (empty)

Response (200):
{
  "id": 1,
  "is_read": true,
  "read_at": "2024-02-13T10:30:00Z"
}
```

---

## Status Flow Diagram

```
Available Delivery
      ↓
   Accept
      ↓
ACCEPTED
      ↓
Update Status: PICKED_UP_OTW
      ↓
Update Status: PICKED_UP
      ↓
Update Status: OTW_TO_BUYER
      ↓
Update Status: ARRIVED
      ↓
   Complete
      ↓
COMPLETED
```

---

## Common Patterns

### Accept and Check Status
```bash
# Accept delivery
curl -X POST http://localhost:8000/api/deliveries/1/accept/ \
  -H "Authorization: Bearer {token}"

# Get updated delivery
curl http://localhost:8000/api/deliveries/1/ \
  -H "Authorization: Bearer {token}"
```

### Update Multiple Statuses
```bash
# Start: PICKED_UP_OTW
curl -X POST http://localhost:8000/api/deliveries/1/update_status/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"status":"PICKED_UP_OTW","notes":"Starting pickup"}'

# Then: PICKED_UP
curl -X POST http://localhost:8000/api/deliveries/1/update_status/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"status":"PICKED_UP","notes":"Picked up goods"}'

# Then: OTW_TO_BUYER
curl -X POST http://localhost:8000/api/deliveries/1/update_status/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"status":"OTW_TO_BUYER","notes":"On the way"}'

# Then: ARRIVED
curl -X POST http://localhost:8000/api/deliveries/1/update_status/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"status":"ARRIVED","notes":"At destination"}'

# Finally: Complete
curl -X POST http://localhost:8000/api/deliveries/1/complete/ \
  -H "Authorization: Bearer {token}"
```

### Error Handling
```javascript
// Example React code
try {
  const response = await acceptDelivery(deliveryId);
  console.log('Success:', response);
} catch (error) {
  if (error.response?.status === 400) {
    console.error('Invalid delivery status:', error.response.data.error);
  } else if (error.response?.status === 403) {
    console.error('Unauthorized:', error.response.data.error);
  } else {
    console.error('Unknown error:', error.message);
  }
}
```

---

## Notification Types

| Type | Trigger | When |
|------|---------|------|
| NEW_DELIVERY | Order approved | When farmer approves an order |
| DELIVERY_EXPIRED | Delivery rejected | When another rider rejects it |
| STATUS_UPDATE | Status changes | Each time delivery status updates |

---

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (invalid data) |
| 403 | Forbidden (not authorized) |
| 404 | Not found |
| 500 | Server error |

---

## Troubleshooting

### "Delivery already accepted"
- Another rider already accepted
- Try getting available deliveries again

### "Cannot accept delivery with status: REJECTED"
- Delivery was already rejected
- Try another available delivery

### "Invalid status transition"
- Status progression wrong (must follow: PICKED_UP_OTW → PICKED_UP → OTW_TO_BUYER → ARRIVED)
- Check current status before updating

### "You are not authorized"
- Make sure you're logged in with rider account
- Check authorization token is valid
- Verify token is in Authorization header

---

## Rate Limiting
Currently: No rate limiting  
Future: May implement rate limiting per rider

---

## API Version
**Current**: 1.0.0

---

**Last Updated**: February 13, 2026  
**For Support**: Contact development team
