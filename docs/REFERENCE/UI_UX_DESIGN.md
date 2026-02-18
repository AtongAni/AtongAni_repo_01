# UI/UX Design & Status System

## Order Status Visual System

### Status Badges & Icons

Each order status has a unique visual representation:

```
┌─────────────────────────────────────────────────────────────┐
│                    ORDER STATUS INDICATORS                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Status: IN_PROGRESS                                        │
│  Icon: ⏳ (Hourglass)                                       │
│  Badge Color: Orange (#FFA500)                              │
│  Badge Background: #FFE0B2 (light orange)                  │
│  Meaning: Farmer is reviewing the order                     │
│  Customer Message: "Awaiting farmer approval..."            │
│                                                              │
│  Status: APPROVED                                           │
│  Icon: ✅ (Check Mark)                                      │
│  Badge Color: Green (#28A745)                               │
│  Badge Background: #C8E6C9 (light green)                   │
│  Meaning: Farmer approved, order confirmed                  │
│  Customer Message: "Order has been approved!"              │
│                                                              │
│  Status: REJECTED                                           │
│  Icon: ❌ (X Mark)                                          │
│  Badge Color: Red (#DC3545)                                 │
│  Badge Background: #FFCDD2 (light red)                     │
│  Meaning: Farmer rejected order                             │
│  Customer Message: "Order rejected - [reason]"             │
│  Action: Items returned to cart automatically              │
│                                                              │
│  Status: COMPLETED                                          │
│  Icon: 🎉 (Party Popper)                                   │
│  Badge Color: Blue (#007BFF)                                │
│  Badge Background: #BBDEFB (light blue)                    │
│  Meaning: Order fulfilled (future use)                      │
│  Customer Message: "Order delivered!"                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Customer Interface (OrdersView)

### Layout Structure

```
┌────────────────────────────────────────────────────────────┐
│                      MY ORDERS                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Order #123                     ⏳ In Progress      │ │
│  │ January 12, 2024               ₱500.00            │ │
│  │                                                      │ │
│  │ [Click to expand details]                           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Order #122                     ✅ Approved        │ │
│  │ January 10, 2024               ₱350.00            │ │
│  │                                                      │ │
│  │ [Click to expand details]                           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Order #121                     ❌ Rejected        │ │
│  │ January 8, 2024                ₱200.00            │ │
│  │                                                      │ │
│  │ [Click to expand details]                           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Expanded Order Details

```
┌────────────────────────────────────────────────────────────┐
│ Order #123                     ⏳ In Progress              │
│ January 12, 2024 at 2:30 PM    ₱500.00                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Items:                                                    │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Organic Tomatoes (10 KG)           ₱250.00          │ │
│ │ From: farmer_john                                    │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                            │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Fresh Lettuce (5 KG)               ₱250.00          │ │
│ │ From: farmer_jane                                    │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                            │
│ Status: ⏳ This order is awaiting farmer approval.       │
│ You will be notified once the farmer responds.            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Rejected Order with Reason

```
┌────────────────────────────────────────────────────────────┐
│ Order #121                     ❌ Rejected                │
│ January 8, 2024 at 10:15 AM    ₱200.00                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Items:                                                    │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Carrots (20 KG)                    ₱200.00          │ │
│ │ From: farmer_bob                                     │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                            │
│ ⚠️ Rejection Reason:                                      │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Only 15 KG available in stock. Please reduce        │ │
│ │ quantity and try again.                              │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                            │
│ ℹ️ Items have been returned to your cart. You can modify  │
│ quantities and try again.                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Farmer Interface (FarmerOrdersManagement)

### Pending Orders List

```
┌────────────────────────────────────────────────────────────┐
│                   ORDER MANAGEMENT                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ⏳ 3 Pending Orders                                      │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Order #124                                           │ │
│  │ Customer: john_doe                                   │ │
│  │ Placed: January 12, 2024 at 2:45 PM                │ │
│  │                                                      │ │
│  │ Items for Your Review:                              │ │
│  │ ┌────────────────────────────────────────────────┐  │ │
│  │ │ Tomatoes (10 KG)            ₱50/KG ₱500.00   │  │ │
│  │ └────────────────────────────────────────────────┘  │ │
│  │                                                      │ │
│  │ Order Total: ₱500.00                               │ │
│  │                                                      │ │
│  │ [✅ Accept Order]  [❌ Reject Order]               │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Order #123                                           │ │
│  │ Customer: jane_smith                                 │ │
│  │ Placed: January 12, 2024 at 1:30 PM                │ │
│  │                                                      │ │
│  │ Items for Your Review:                              │ │
│  │ ┌────────────────────────────────────────────────┐  │ │
│  │ │ Lettuce (5 KG)              ₱30/KG ₱150.00    │  │ │
│  │ │ Spinach (3 KG)              ₱40/KG ₱120.00    │  │ │
│  │ └────────────────────────────────────────────────┘  │ │
│  │                                                      │ │
│  │ Order Total: ₱270.00                               │ │
│  │                                                      │ │
│  │ [✅ Accept Order]  [❌ Reject Order]               │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Rejection Form (When Reject is Clicked)

```
┌────────────────────────────────────────────────────────────┐
│ Order #123                                                 │
│ Customer: jane_smith                                       │
│ Placed: January 12, 2024 at 1:30 PM                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Items for Your Review:                                    │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Lettuce (5 KG)              ₱30/KG ₱150.00        │ │
│ │ Spinach (3 KG)              ₱40/KG ₱120.00        │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                            │
│ Order Total: ₱270.00                                     │
│                                                            │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Why are you rejecting this order?                    │ │
│ │                                                      │ │
│ │ [                                                  ] │ │
│ │ [  Spinach out of stock, only have 2 KG available ] │ │
│ │ [                                                  ] │ │
│ │                                                      │ │
│ │ [Confirm Rejection]  [Cancel]                       │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Checkout Flow Diagram

```
CUSTOMER SIDE                          FARMER SIDE
═════════════════════════════════════════════════════════════

1. View Cart
   ├─ Items listed
   └─ Total calculated
                                       
2. Click "Proceed to Checkout"
   │
   ├─ CartItem objects converted to Order + OrderItem
   ├─ Order status set to IN_PROGRESS
   ├─ Show order confirmation
   │  ├─ Order ID displayed
   │  ├─ Status: ⏳ In Progress
   │  └─ Items summarized
   │                                  
3. Monitor Order Status                                    
   (Polling every 5 seconds)          
   │
   ├─ Check Order.status              
   │  ├─ IN_PROGRESS: Wait message    
   │  ├─ APPROVED: Success message    
   │  └─ REJECTED: Failure + items to cart
                                       
                                       1. Check Pending Orders
                                          (Polling every 3 seconds)
                                          
                                       2. See Order in "Pending"
                                          ├─ Customer name
                                          ├─ Order ID
                                          ├─ Items list
                                          └─ Order total
                                          
                                       3. Review & Make Decision
                                          │
                                          ├─ [Accept Order]
                                          │  ├─ Check stock
                                          │  ├─ Reduce quantity
                                          │  ├─ Delete post if 0
                                          │  ├─ Set status APPROVED
                                          │  └─ Clear customer cart
                                          │
                                          └─ [Reject Order]
                                             ├─ Ask for reason
                                             ├─ Set status REJECTED
                                             ├─ Return items to cart
                                             └─ Store rejection reason
                                       
4. Order Complete
   │
   ├─ APPROVED: Order confirmed
   │  └─ Items ready for delivery
   │
   └─ REJECTED: Back in cart
      └─ Items available to modify
```

## Color Scheme

### Status Colors
```css
/* In Progress */
.status-in-progress {
  background-color: #fffaf0;    /* Light orange background */
  border-left-color: #ffa500;   /* Orange border */
}

/* Approved */
.status-approved {
  background-color: #f0fff4;    /* Light green background */
  border-left-color: #28a745;   /* Green border */
}

/* Rejected */
.status-rejected {
  background-color: #fff5f5;    /* Light red background */
  border-left-color: #dc3545;   /* Red border */
}

/* Completed */
.status-completed {
  background-color: #f0f8ff;    /* Light blue background */
  border-left-color: #007bff;   /* Blue border */
}
```

### Badge Colors
```css
.status-badge.status-in-progress {
  background-color: #ffe0b2;    /* Orange background */
  color: #e65100;               /* Dark orange text */
}

.status-badge.status-approved {
  background-color: #c8e6c9;    /* Green background */
  color: #1b5e20;               /* Dark green text */
}

.status-badge.status-rejected {
  background-color: #ffcdd2;    /* Red background */
  color: #b71c1c;               /* Dark red text */
}
```

## Responsive Design

### Mobile Layout (< 768px)

#### Customer Orders
```
┌──────────────────────┐
│  Order #123          │
│  ⏳ In Progress     │
│  ₱500.00             │
│                      │
│  [Tap to expand]     │
└──────────────────────┘
```

#### Farmer Orders
```
┌──────────────────────┐
│ Order #123           │
│ john_doe             │
│ Jan 12, 2:45 PM      │
│                      │
│ Tomatoes             │
│ 10 KG - ₱500.00     │
│                      │
│ [Accept] [Reject]    │
└──────────────────────┘
```

### Tablet Layout (768px - 1024px)

Sidebar navigation + Main content area with proper spacing

### Desktop Layout (> 1024px)

Full-width cards with expanded content, side-by-side layouts

## Animation & Transitions

### Order Status Change
```css
/* Smooth fade-in when order status updates */
transition: all 0.3s ease;

/* Status badge color change */
.status-badge {
  transition: background-color 0.3s ease, color 0.3s ease;
}
```

### Expandable Details
```css
/* Slide down animation for order expansion */
@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 500px;
  }
}
```

### Button Interactions
```css
/* Hover state */
button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Active state */
button:active {
  transform: translateY(0);
}
```

## Accessibility Features

1. **Semantic HTML**
   - Proper heading hierarchy (h3, h4, h5)
   - List elements for order items
   - Button elements for actions

2. **ARIA Labels**
   - Button purposes clearly stated
   - Status indicators labeled
   - Loading states indicated

3. **Color Contrast**
   - Text color contrast ratio ≥ 4.5:1
   - Badge text contrasts with background
   - Status indicators not color-only

4. **Keyboard Navigation**
   - All buttons and links keyboard accessible
   - Tab order follows logical flow
   - Focus indicators visible

5. **Mobile Friendly**
   - Touch-friendly button sizes (min 44px)
   - Proper spacing for touch targets
   - Readable font sizes on all devices

## Print Styles

Orders can be printed for reference:
```css
@media print {
  .hide-on-print { display: none; }
  .order-card { page-break-inside: avoid; }
  colors simplified to grayscale
}
```
