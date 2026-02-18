# 360px Mobile CSS Optimization - Code Reference

## Before & After Examples

### 1. Dashboard Header
```css
/* BEFORE - Not optimized for 360px */
.dashboard-header {
  padding: 12px 20px;
}

.dashboard-header h1 {
  font-size: 20px;
}

.user-avatar {
  width: 42px;
  height: 42px;
}

/* AFTER - 360px optimized */
@media (max-width: 360px) {
  .dashboard-header {
    padding: 10px 0;
  }

  .dashboard-header h1 {
    font-size: 16px;
    margin: 0;
  }

  .user-avatar {
    width: 36px;
    height: 36px;
  }
}
```

### 2. Tab Navigation
```css
/* BEFORE - Breaks on 360px */
.dashboard-tabs {
  display: flex;
}

.tab-btn {
  flex: 1;
  min-width: 90px;
  padding: 16px 14px;
  font-size: 13px;
}

/* AFTER - Scrollable on 360px */
@media (max-width: 360px) {
  .dashboard-tabs {
    overflow-x: auto;
    white-space: nowrap;
  }

  .tab-btn {
    flex: 0 0 auto;
    min-width: 70px;
    padding: 12px 8px;
    font-size: 11px;
    white-space: nowrap;
  }
}
```

### 3. Post Cards
```css
/* BEFORE - Overlapping elements */
.post-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-radius: 8px;
}

.post-avatar {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.post-footer {
  display: flex;
  gap: 12px;
}

.action-btn {
  min-width: 100px;
  padding: 9px 10px;
  font-size: 12px;
}

/* AFTER - Optimized layout */
@media (max-width: 360px) {
  .post-card {
    gap: 0;
    padding: 10px;
    border-radius: 4px;
  }

  .post-avatar {
    width: 32px;
    height: 32px;
  }

  .post-footer {
    gap: 6px;
    flex-wrap: wrap;
  }

  .action-btn {
    flex: 1;
    min-width: 60px;
    padding: 8px 8px;
    font-size: 11px;
  }
}
```

### 4. Form Layouts
```css
/* BEFORE - Side-by-side inputs */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-input {
  padding: 12px 10px;
  font-size: 14px;
}

/* AFTER - Full-width stacked */
@media (max-width: 360px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .form-input {
    padding: 10px 8px;
    font-size: 15px; /* Prevent zoom on iOS */
    border-radius: 4px;
  }
}
```

### 5. Cart Items
```css
/* BEFORE - Horizontal layout */
.cart-item {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 12px;
}

.qty-btn {
  width: 36px;
  height: 36px;
  font-size: 14px;
}

/* AFTER - Wrapped layout */
@media (max-width: 360px) {
  .cart-item {
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px;
  }

  .cart-item-info {
    flex-basis: 100%;
  }

  .qty-btn {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }

  .cart-item-quantity {
    flex: 1;
    min-width: 60px;
  }
}
```

### 6. Filter Bars
```css
/* BEFORE - All visible */
.feed-filters {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 8px 12px;
  font-size: 12px;
}

/* AFTER - Scrollable */
@media (max-width: 360px) {
  .feed-filters {
    gap: 4px;
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 4px;
  }

  .filter-btn {
    flex-shrink: 0;
    padding: 5px 8px;
    font-size: 10px;
  }
}
```

### 7. Table Layouts (Admin)
```css
/* BEFORE - Fixed sizing */
.activity-table {
  font-size: 12px;
}

.activity-table th,
.activity-table td {
  padding: 8px;
}

/* AFTER - Compact on mobile */
@media (max-width: 360px) {
  .activity-table {
    font-size: 10px;
    border-radius: 4px;
    overflow: hidden;
  }

  .activity-table th {
    font-size: 10px;
    padding: 6px 4px;
  }

  .activity-table td {
    padding: 6px 4px;
  }
}
```

### 8. Button Groups
```css
/* BEFORE - Stacked buttons */
.farmer-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.approve-btn,
.reject-btn {
  width: 100%;
  padding: 12px;
}

/* AFTER - Space-efficient layout */
@media (max-width: 360px) {
  .farmer-actions {
    flex-direction: row;
    gap: 6px;
  }

  .approve-btn,
  .reject-btn {
    flex: 1;
    padding: 8px 6px;
    font-size: 11px;
    min-height: 36px;
  }
}
```

### 9. Modal/Overlay
```css
/* BEFORE - Large modal */
.image-modal-overlay {
  padding: 16px;
}

.image-modal-img {
  max-height: 50vh;
  padding: 8px;
}

/* AFTER - Compact modal */
@media (max-width: 360px) {
  .image-modal-overlay {
    padding: 4px;
  }

  .image-modal-img {
    max-height: 40vh;
    padding: 4px;
  }

  .image-modal-close {
    width: 28px;
    height: 28px;
    font-size: 18px;
  }
}
```

### 10. Stats Display
```css
/* BEFORE - Multi-column grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-number {
  font-size: 2.5rem;
}

/* AFTER - Single column */
@media (max-width: 360px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .stat-number {
    font-size: 16px;
    margin-bottom: 4px;
  }

  .stat-label {
    font-size: 12px;
  }
}
```

## Common Patterns to Apply

### Pattern 1: Flexible Buttons
```css
/* Always apply on 360px */
.action-button {
  flex: 1;
  min-width: 60px;  /* Prevent too-small buttons */
  min-height: 36px; /* Touch target minimum */
  font-size: 11px;
  padding: 8px 6px;
}
```

### Pattern 2: Stacked Layouts
```css
/* Convert side-by-side to stacked */
.two-column {
  grid-template-columns: 1fr;  /* Changed from 1fr 1fr */
  gap: 10px;                   /* Reduced gap */
}
```

### Pattern 3: Scrollable Containers
```css
/* For anything that might overflow */
.horizontal-scroll {
  overflow-x: auto;
  white-space: nowrap;
  scrollbar-width: thin;
}

.horizontal-scroll::-webkit-scrollbar {
  height: 4px;
}
```

### Pattern 4: Font Optimization
```css
/* 360px typography */
/* Headers: 14-18px */
/* Body: 11-12px */
/* Small: 9-10px */
/* Never go below 9px */
```

### Pattern 5: Spacing Optimization
```css
/* 360px spacing */
/* Card padding: 8-12px */
/* Section gap: 6-10px */
/* Internal margin: 4-8px */
```

## Utility Classes You Can Create

```css
/* Optional utility classes for 360px optimization */
@media (max-width: 360px) {
  .mobile-full-width {
    width: 100%;
  }

  .mobile-single-col {
    grid-template-columns: 1fr;
  }

  .mobile-scroll-x {
    overflow-x: auto;
  }

  .mobile-s-text {
    font-size: 11px;
  }

  .mobile-xs-text {
    font-size: 10px;
  }

  .mobile-tight-gap {
    gap: 6px;
  }

  .mobile-min-btn {
    min-height: 36px;
  }

  .mobile-touch-target {
    min-height: 40px;
  }
}
```

## Testing CSS Changes

### Step 1: Chrome DevTools
```javascript
// In console on 360px viewport
document.body.style.border = '2px solid red'; // Visual check
```

### Step 2: Mobile Testing
- Test on actual device OR
- Use DevTools device emulation
- Rotate between portrait/landscape

### Step 3: Validation
- Run through CSS validator
- Check for overflow on content
- Verify all buttons are tappable

## Performance Tips

1. **Minimize CSS**: Ensure 360px rules don't create unnecessary bloat
2. **Mobile-First**: Start with 360px then enhance upward
3. **Media Query Order**: Keep 360px breakpoint last
4. **Reusability**: Use variables for common sizes

```css
/* Example with CSS variables */
:root {
  --mobile-padding: 16px;
  --mobile-gap: 12px;
}

@media (max-width: 360px) {
  :root {
    --mobile-padding: 8px;
    --mobile-gap: 6px;
  }
}

.card {
  padding: var(--mobile-padding);
  gap: var(--mobile-gap);
}
```

---

**Reference Document**: 360px CSS Optimization Patterns
**Last Updated**: February 17, 2026
**Status**: Production Ready
