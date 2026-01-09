import { useEffect, useState } from "react";
import { getCart, removeFromCart, updateCartItem, checkoutCart } from "../api/cart";
import "./CartView.css";

export default function CartView() {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [checkingOut, setCheckingOut] = useState(false);

  useEffect(() => {
    loadCart();
  }, []);

  async function loadCart() {
    try {
      const res = await getCart();
      setCartItems(res.data || []);
      setError("");
    } catch (err) {
      setError("Failed to load cart");
      console.log(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRemoveItem(cartItemId) {
    try {
      await removeFromCart(cartItemId);
      await loadCart();
    } catch (err) {
      setError("Failed to remove item");
    }
  }

  async function handleUpdateQuantity(cartItemId, quantity) {
    if (quantity < 1) {
      handleRemoveItem(cartItemId);
      return;
    }

    try {
      await updateCartItem(cartItemId, quantity);
      await loadCart();
    } catch (err) {
      setError("Failed to update quantity");
    }
  }

  async function handleCheckout() {
    if (cartItems.length === 0) {
      setError("Cart is empty");
      return;
    }

    setCheckingOut(true);
    setError("");

    try {
      await checkoutCart();
      setCartItems([]);
      // Show success - in real app, navigate to order confirmation
      alert("Order placed successfully!");
    } catch (err) {
      setError(err?.response?.data?.detail || "Checkout failed");
    } finally {
      setCheckingOut(false);
    }
  }

  if (loading) {
    return <div className="cart-view"><div className="loading">Loading cart...</div></div>;
  }

  const total = cartItems.reduce((sum, item) => sum + (item.post.price * item.quantity || 0), 0);

  return (
    <div className="cart-view">
      <h3>Shopping Cart</h3>

      {error && <div className="cart-error">{error}</div>}

      {cartItems.length === 0 ? (
        <div className="empty-cart">
          <p>Your cart is empty</p>
          <p className="empty-cart-hint">Add items from farmer posts to get started</p>
        </div>
      ) : (
        <>
          <div className="cart-items">
            {cartItems.map((item) => (
              <div key={item.id} className="cart-item">
                <div className="cart-item-info">
                  <h4 className="cart-item-title">{item.post.title}</h4>
                  <p className="cart-item-farmer">from {item.post.author_name || "Farmer"}</p>
                  <p className="cart-item-price">₱{item.post.price}</p>
                </div>

                <div className="cart-item-quantity">
                  <button
                    onClick={() => handleUpdateQuantity(item.id, item.quantity - 0.1)}
                    className="qty-btn"
                    aria-label="Decrease quantity"
                  >
                    −
                  </button>
                  <input
                    type="number"
                    value={item.quantity}
                    onChange={(e) => handleUpdateQuantity(item.id, parseFloat(e.target.value))}
                    className="qty-input"
                    step="0.01"
                    min="0"
                  />
                  <span className="qty-unit">{item.unit === 'KG' ? 'kg' : 'g'}</span>
                  <button
                    onClick={() => handleUpdateQuantity(item.id, item.quantity + 0.1)}
                    className="qty-btn"
                    aria-label="Increase quantity"
                  >
                    +
                  </button>
                </div>

                <div className="cart-item-subtotal">
                  <p>₱{(item.post.price * item.quantity).toFixed(2)}</p>
                  <button
                    onClick={() => handleRemoveItem(item.id)}
                    className="remove-btn"
                    aria-label="Remove item"
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <div className="summary-row">
              <span>Subtotal:</span>
              <span>₱{total.toFixed(2)}</span>
            </div>
            <div className="summary-row">
              <span>Shipping:</span>
              <span>Calculated at checkout</span>
            </div>
            <div className="summary-row total-row">
              <span>Total:</span>
              <span>₱{total.toFixed(2)}</span>
            </div>
          </div>

          <button
            onClick={handleCheckout}
            disabled={checkingOut || cartItems.length === 0}
            className="checkout-btn"
          >
            {checkingOut ? "Processing..." : "Proceed to Checkout"}
          </button>
        </>
      )}
    </div>
  );
}
