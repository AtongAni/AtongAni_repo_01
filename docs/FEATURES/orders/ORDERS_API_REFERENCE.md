# Orders Feature - API Reference

## Base URL
```
http://127.0.0.1:8000/api/
```

**Authentication**: Required for all endpoints (JWT Bearer Token)

---

## Endpoints Overview

| Method | Endpoint | Purpose | Role |
|--------|----------|---------|------|
| `GET` | `/orders/my_orders/` | Get all customer orders | Customer |
| `GET` | `/orders/my_pending_orders/` | Get farmer's pending approvals | Farmer |
| `GET` | `/orders/{id}/` | Get specific order details | Any |
| `POST` | `/orders/checkout/` | Create order from cart items | Customer |
| `POST` | `/orders/{id}/approve/` | Farmer approves order | Farmer |
| `POST` | `/orders/{id}/reject/` | Farmer rejects order with reason | Farmer |

---

## Detailed Endpoint Documentation

### 1. Get Customer's All Orders
**Endpoint**: `GET /orders/my_orders/`

**Authentication**: Required (JWT Bearer Token)

**Description**: Retrieve all orders for the authenticated customer, including approved, rejected, and completed orders.

**Request Headers**:
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

**Request Body**: None

**Response (200 OK)**:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "customer": 2,
      "customer_name": "Juan dela Cruz",
      "status": "APPROVED",
      "created_at": "2026-01-12T10:30:00Z",
      "updated_at": "2026-01-12T10:35:00Z",
      "rejection_reason": null,
      "total_amount": "650.00",
      "items": [
        {
          "id": 1,
          "post": 5,
          "post_title": "Tomatoes",
          "farmer_name": "Maria's Farm",
          "quantity": "5.00",
          "price": "100.00",
          "total_price": "500.00",
          "unit": "kg"
        },
        {
          "id": 2,
          "post": 8,
          "post_title": "Corn",
          "farmer_name": "Green Valley Farm",
          "quantity": "3.00",
          "price": "50.00",
          "total_price": "150.00",
          "unit": "bundles"
        }
      ]
    }
  ]
}
```

**Response (401 Unauthorized)**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 2. Get Farmer's Pending Orders
**Endpoint**: `GET /orders/my_pending_orders/`

**Authentication**: Required (Farmer/Staff user)

**Description**: Retrieve all pending orders awaiting farmer approval. Only accessible by farmers (is_staff=true).

**Request Headers**:
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

**Request Body**: None

**Response (200 OK)**:
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "customer": 3,
      "customer_name": "Rosa Santos",
      "status": "IN_PROGRESS",
      "created_at": "2026-01-12T11:00:00Z",
      "updated_at": "2026-01-12T11:00:00Z",
      "rejection_reason": null,
      "total_amount": "450.00",
      "items": [
        {
          "id": 3,
          "post": 12,
          "post_title": "Lettuce",
          "farmer_name": "Organic Farms Co.",
          "quantity": "2.00",
          "price": "150.00",
          "total_price": "300.00",
          "unit": "heads"
        },
        {
          "id": 4,
          "post": 15,
          "post_title": "Carrots",
          "farmer_name": "Organic Farms Co.",
          "quantity": "3.00",
          "price": "50.00",
          "total_price": "150.00",
          "unit": "kg"
        }
      ]
    }
  ]
}
```

**Response (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 3. Get Order Details
**Endpoint**: `GET /orders/{id}/`

**Authentication**: Required

**Parameters**:
- `id` (path, required): Order ID

**Description**: Get detailed information about a specific order.

**Request Headers**:
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

**Request**:
```
GET /orders/1/
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "customer": 2,
  "customer_name": "Juan dela Cruz",
  "status": "APPROVED",
  "created_at": "2026-01-12T10:30:00Z",
  "updated_at": "2026-01-12T10:35:00Z",
  "rejection_reason": null,
  "total_amount": "650.00",
  "items": [
    {
      "id": 1,
      "post": 5,
      "post_title": "Tomatoes",
      "farmer_name": "Maria's Farm",
      "quantity": "5.00",
      "price": "100.00",
      "total_price": "500.00",
      "unit": "kg"
    }
  ]
}
```

**Response (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

---

### 4. Checkout Order (Create Order from Cart)
**Endpoint**: `POST /orders/checkout/`

**Authentication**: Required

**Description**: Create a new order from the authenticated customer's cart. Sets order status to IN_PROGRESS and clears the cart.

**Request Headers**:
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

**Request Body**: Empty (uses authenticated user's cart)
```json
{}
```

**Response (201 Created)**:
```json
{
  "id": 5,
  "customer": 2,
  "customer_name": "Juan dela Cruz",
  "status": "IN_PROGRESS",
  "created_at": "2026-01-12T14:20:00Z",
  "updated_at": "2026-01-12T14:20:00Z",
  "rejection_reason": null,
  "total_amount": "950.00",
  "items": [
    {
      "id": 10,
      "post": 5,
      "post_title": "Tomatoes",
      "farmer_name": "Maria's Farm",
      "quantity": "5.00",
      "price": "100.00",
      "total_price": "500.00",
      "unit": "kg"
    },
    {
      "id": 11,
      "post": 20,
      "post_title": "Cabbage",
      "farmer_name": "Fresh Greens",
      "quantity": "3.00",
      "price": "150.00",
      "total_price": "450.00",
      "unit": "heads"
    }
  ]
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Cart is empty"
}
```

**Response (401 Unauthorized)**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 5. Approve Order (Farmer)
**Endpoint**: `POST /orders/{id}/approve/`

**Authentication**: Required (Farmer/Staff)

**Parameters**:
- `id` (path, required): Order ID to approve

**Description**: Farmer approves an order. Changes status to APPROVED, reduces inventory by ordered quantity, and clears customer's cart.

**Request Headers**:
```json
{
  "Authorization": "Bearer {farmer_token}",
  "Content-Type": "application/json"
}
```

**Request Body**: Empty
```json
{}
```

**Request**:
```
POST /orders/2/approve/
```

**Response (200 OK)**:
```json
{
  "id": 2,
  "customer": 3,
  "customer_name": "Rosa Santos",
  "status": "APPROVED",
  "created_at": "2026-01-12T11:00:00Z",
  "updated_at": "2026-01-12T11:05:00Z",
  "rejection_reason": null,
  "total_amount": "450.00",
  "items": [
    {
      "id": 3,
      "post": 12,
      "post_title": "Lettuce",
      "farmer_name": "Organic Farms Co.",
      "quantity": "2.00",
      "price": "150.00",
      "total_price": "300.00",
      "unit": "heads"
    }
  ]
}
```

**Response (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Response (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

---

### 6. Reject Order (Farmer)
**Endpoint**: `POST /orders/{id}/reject/`

**Authentication**: Required (Farmer/Staff)

**Parameters**:
- `id` (path, required): Order ID to reject

**Description**: Farmer rejects an order with explanation. Changes status to REJECTED, stores rejection reason, and returns items to customer's cart.

**Request Headers**:
```json
{
  "Authorization": "Bearer {farmer_token}",
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "reason": "Out of stock on fresh lettuce"
}
```

**Request**:
```
POST /orders/2/reject/
Content-Type: application/json

{
  "reason": "Out of stock on fresh lettuce"
}
```

**Response (200 OK)**:
```json
{
  "id": 2,
  "customer": 3,
  "customer_name": "Rosa Santos",
  "status": "REJECTED",
  "created_at": "2026-01-12T11:00:00Z",
  "updated_at": "2026-01-12T11:06:00Z",
  "rejection_reason": "Out of stock on fresh lettuce",
  "total_amount": "450.00",
  "items": [
    {
      "id": 3,
      "post": 12,
      "post_title": "Lettuce",
      "farmer_name": "Organic Farms Co.",
      "quantity": "2.00",
      "price": "150.00",
      "total_price": "300.00",
      "unit": "heads"
    }
  ]
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Reason is required"
}
```

**Response (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Data Types

### Order Object
```json
{
  "id": "integer",
  "customer": "integer (User ID)",
  "customer_name": "string",
  "status": "string (PENDING|IN_PROGRESS|APPROVED|REJECTED|COMPLETED)",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime",
  "rejection_reason": "string or null",
  "total_amount": "string (decimal with 2 places)",
  "items": "[OrderItem]"
}
```

### OrderItem Object
```json
{
  "id": "integer",
  "post": "integer (Post ID)",
  "post_title": "string",
  "farmer_name": "string",
  "quantity": "string (decimal)",
  "price": "string (decimal with 2 places)",
  "total_price": "string (decimal with 2 places)",
  "unit": "string (kg, bundles, pieces, etc.)"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Description of what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- **Polling**: Recommended interval of 3-5 seconds (customer 5s, farmer 3s)
- **No Hard Limit**: API does not enforce rate limiting
- **Best Practice**: Implement exponential backoff on errors

---

## Authentication

All endpoints require JWT Bearer token authentication.

**Header Format**:
```
Authorization: Bearer {access_token}
```

**Obtaining Token**: Use the authentication endpoints (login) to get JWT tokens.

---

## CORS Headers

```
Access-Control-Allow-Origin: http://localhost:5173 (or configured origin)
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## Implementation Examples

### JavaScript/Fetch

**Checkout Order**:
```javascript
const response = await fetch('http://127.0.0.1:8000/api/orders/checkout/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({})
});

const order = await response.json();
```

**Get Pending Orders (Farmer)**:
```javascript
const response = await fetch('http://127.0.0.1:8000/api/orders/my_pending_orders/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

const orders = await response.json();
```

**Approve Order**:
```javascript
const response = await fetch(`http://127.0.0.1:8000/api/orders/${orderId}/approve/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({})
});

const updatedOrder = await response.json();
```

**Reject Order**:
```javascript
const response = await fetch(`http://127.0.0.1:8000/api/orders/${orderId}/reject/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    reason: "Out of stock on fresh tomatoes"
  })
});

const rejectedOrder = await response.json();
```

---

## Pagination

All list endpoints support pagination:

**Query Parameters**:
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10)

**Example**:
```
GET /orders/my_orders/?page=2&page_size=20
```

**Response**:
```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/orders/my_orders/?page=3&page_size=20",
  "previous": "http://127.0.0.1:8000/api/orders/my_orders/?page=1&page_size=20",
  "results": [...]
}
```

---

**Last Updated**: January 12, 2026  
**Version**: 1.0  
**Status**: ✅ Complete & Production Ready
