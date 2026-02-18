# Orders Feature - Farmer Dashboard UI Guide

## Overview

The **Farmer Orders Management** component provides a dashboard where farmers can review and process customer orders in real-time.

**Component**: `web/src/components/FarmerOrdersManagement.jsx`  
**Styling**: `web/src/components/FarmerOrdersManagement.css`

---

## User Interface Layout

### Header Section
```
┌─────────────────────────────────────────┐
│           Order Management              │  ← Title showing pending orders count
└─────────────────────────────────────────┘
```

### Messages Section
- **Success Messages** (green background)
  - "Order approved successfully!"
  - "Order rejected. Items returned to customer's cart."
  - Auto-dismisses after 3 seconds

- **Error Messages** (red background)
  - "Failed to approve order"
  - "Failed to reject order"
  - "Please provide a reason for rejection"
  - Dismisses on next action

### Empty State
When no pending orders:
```
┌─────────────────────────────────────────┐
│      No pending orders                  │
│  Orders will appear here when           │
│  customers place them                   │
└─────────────────────────────────────────┘
```

### Order Card Layout

Each pending order displays:

```
┌───────────────────────────────────────────────────────────┐
│  Order #1234                                              │
│  Customer: Juan dela Cruz                                 │
│  Jan 12, 2026, 2:30 PM                                   │
├───────────────────────────────────────────────────────────┤
│  Items for Your Review:                                   │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Tomatoes                                            │ │
│  │ Quantity: 5 kg                                      │ │
│  │ Unit Price: ₱100         Subtotal: ₱500.00        │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Corn                                                │ │
│  │ Quantity: 3 bundles                                 │ │
│  │ Unit Price: ₱50          Subtotal: ₱150.00         │ │
│  └─────────────────────────────────────────────────────┘ │
├───────────────────────────────────────────────────────────┤
│  Order Total: ₱650.00                                     │
├───────────────────────────────────────────────────────────┤
│  ┌──────────────────┐     ┌────────────────┐             │
│  │ ✅ Accept Order  │     │ ❌ Reject Order│             │
│  └──────────────────┘     └────────────────┘             │
└───────────────────────────────────────────────────────────┘
```

---

## Action Buttons

### Accept Order Button (✅)
- **Label**: "✅ Accept Order"
- **Color**: Green background
- **Click Action**:
  1. Immediately approves the order
  2. Reduces inventory by ordered quantity
  3. Clears customer's cart
  4. Sets order status to APPROVED
  5. Removes order from pending list
  6. Shows success message
- **Error Handling**: Displays error message if request fails
- **Tooltip**: "Approve and process this order"

### Reject Order Button (❌)
- **Label**: "❌ Reject Order"
- **Color**: Red background
- **Click Action**: Opens rejection form below buttons
- **Tooltip**: "Reject this order"

---

## Rejection Form

When farmer clicks "Reject Order", form appears:

```
┌────────────────────────────────────────────┐
│  ┌──────────────────────────────────────┐  │
│  │ Why are you rejecting this order?   │  │
│  │                                      │  │
│  │  [Textarea - Multi-line input]       │  │
│  │  - Out of stock                      │  │
│  │  - Quality issues                    │  │
│  │  - Delivery problems                 │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────┐ ┌──────────┐    │
│  │ Confirm Rejection    │ │  Cancel  │    │
│  └──────────────────────┘ └──────────┘    │
└────────────────────────────────────────────┘
```

### Rejection Form Features
- **Textarea**
  - Placeholder: "Why are you rejecting this order?"
  - Multi-line input for detailed explanation
  - Required field (must have content)
  - Auto-focuses when form opens

- **Confirm Rejection Button**
  - Color: Dark red
  - Validation: Requires non-empty reason
  - Error: Shows "Please provide a reason for rejection"
  - Success: 
    1. Submits rejection with reason
    2. Returns items to customer's cart
    3. Sets order status to REJECTED
    4. Shows success message
    5. Closes form and reloads order list

- **Cancel Button**
  - Color: Gray
  - Action: Closes form without submitting
  - Clears textarea content

---

## Real-Time Updates

### Polling Mechanism
- **Interval**: Every 3 seconds
- **Trigger**: Page load + automatic refresh
- **Updates**: Fetches latest pending orders
- **Refresh**: Entire order list re-renders with new data

### Status Indicator
- **Loading State**: Shows "Loading pending orders..." initially
- **Refresh Indicator**: No visible spinner (background polling)
- **Error Handling**: Continues polling even if one request fails

---

## Data Display Details

### Order Header
- **Order ID**: Displays as "Order #1234"
- **Customer Name**: "Customer: {name}"
- **Timestamp**: Formatted date and time (locale-specific)

### Order Items Section
For each item in the order:
- **Product Name**: Item title from the product listing
- **Quantity & Unit**: "Quantity: 5 kg" or "Quantity: 3 bundles"
- **Unit Price**: ₱{price} (formatted with 2 decimals)
- **Subtotal**: ₱{total_price} (formatted with 2 decimals)

### Order Total
- **Label**: "Order Total:"
- **Amount**: Bold, formatted with 2 decimals
- **Currency**: Philippine Peso (₱) symbol

---

## Mobile Responsiveness

### Responsive Design
- **Large Screens** (≥1024px): 
  - Full-width order cards
  - Side-by-side buttons
  - Expanded item details

- **Tablet** (768px - 1023px):
  - Adjusted padding and margins
  - Stacked buttons if needed
  - Readable font sizes

- **Mobile** (< 768px):
  - Full-width cards with padding
  - Stacked action buttons
  - Touch-friendly button sizes (min 44px height)
  - Responsive text sizing

### Touch Interactions
- Buttons have larger tap targets
- Rejection textarea is easy to interact with on mobile
- Form is fully visible without excessive scrolling
- Message notifications are visible without scroll

---

## Color Scheme

```css
/* Success/Accept */
Background: #4CAF50 (Green)
Text: White
Hover: #45a049

/* Reject/Error */
Background: #f44336 (Red)
Text: White
Hover: #da190b

/* Secondary/Cancel */
Background: #9E9E9E (Gray)
Text: White
Hover: #7d7d7d

/* Messages */
Success Message: #4CAF50 background, white text
Error Message: #f44336 background, white text

/* Card Background */
White background with light shadow
Border: None or very subtle
```

---

## Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Navigate between buttons and form elements |
| `Enter` | Submit form or activate button |
| `Escape` | Close rejection form (if implemented) |
| `Space` | Activate button when focused |

---

## Features Summary

✅ **Accept Order with One Click**
- Immediate approval
- Inventory automatically updated
- Customer cart cleared
- Success message shown

✅ **Reject Order with Reason**
- Rejection form with textarea
- Required reason validation
- Items returned to customer's cart
- Success feedback

✅ **Real-Time Order Updates**
- Polls every 3 seconds
- Automatic list refresh
- Shows new orders immediately

✅ **Clear Order Information**
- Customer name and order ID
- Individual item details with prices
- Order total amount
- Proper timestamp display

✅ **Error Handling**
- Shows error messages
- Graceful failure handling
- Continues polling on errors

✅ **Responsive Design**
- Works on desktop, tablet, mobile
- Touch-friendly interactions
- Readable on all screen sizes

---

## Common Workflows

### Accepting an Order
1. Farmer views pending orders list
2. Reviews customer name, items, and total
3. Clicks "✅ Accept Order" button
4. Order is approved and removed from pending list
5. Success message appears: "Order approved successfully!"
6. Inventory is updated in the system
7. Customer's cart is cleared

### Rejecting an Order
1. Farmer views pending orders list
2. Reviews order details
3. Clicks "❌ Reject Order" button
4. Rejection form appears with textarea
5. Farmer types reason (e.g., "Out of stock")
6. Farmer clicks "Confirm Rejection" button
7. Order is rejected and removed from list
8. Success message appears: "Order rejected. Items returned to customer's cart."
9. Items are automatically added back to customer's cart

### Monitoring Multiple Orders
1. Farmer leaves dashboard open
2. Dashboard polls every 3 seconds automatically
3. New orders appear in the list
4. Farmer can accept/reject as they work
5. Previously processed orders disappear from list
6. Real-time feedback without manual refresh

---

## Accessibility Features

- **Semantic HTML**: Proper heading hierarchy (h3, h4, h5)
- **Button Labels**: Clear, descriptive text with icons
- **Form Labels**: Associated textarea with placeholder text
- **Color Contrast**: Text meets WCAG AA standards
- **Focus States**: Visible focus indicators for keyboard navigation
- **ARIA Labels**: Title attributes on buttons for screen readers
- **Error Messages**: Clear, actionable error text

---

## Performance Considerations

- **Polling Interval**: 3-second refresh is responsive yet efficient
- **Data Optimization**: Only fetches pending orders (filtered server-side)
- **Rendering**: React efficiently updates only changed orders
- **Network**: Minimal payload size for polling requests
- **CPU**: No heavy computations on client-side

---

**Last Updated**: January 12, 2026  
**Version**: 1.0  
**Status**: ✅ Complete & Production Ready
