import { useState } from "react";
import { deletePost } from "../api/posts";
import CommentsSection from "./CommentsSection";
import "./PostCard.css";

export default function PostCard({ post, user, onRefresh }) {
  const [showComments, setShowComments] = useState(false);
  const [cartLoading, setCartLoading] = useState(false);
  const [cartError, setCartError] = useState("");
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [showQuantitySelector, setShowQuantitySelector] = useState(false);
  const [selectedQuantity, setSelectedQuantity] = useState("");

  const isOwner = user?.id === post?.author_id;
  const canAddToCart = post?.price && !isOwner;

  const handleAddToCart = async () => {
    if (!post?.id) return;
    
    if (!selectedQuantity || selectedQuantity <= 0) {
      setCartError("Please enter a valid quantity");
      return;
    }

    if (parseFloat(selectedQuantity) > parseFloat(post.quantity)) {
      setCartError(`Maximum available: ${post.quantity} ${post.unit === 'KG' ? 'kg' : 'g'}`);
      return;
    }
    
    setCartLoading(true);
    setCartError("");
    
    try {
      const { addToCart } = await import("../api/cart");
      await addToCart(post.id, parseFloat(selectedQuantity));
      setCartError("✓ Added to cart");
      setShowQuantitySelector(false);
      setSelectedQuantity("");
      setTimeout(() => setCartError(""), 2000);
    } catch (err) {
      setCartError(err?.response?.data?.error || "Failed to add to cart");
    } finally {
      setCartLoading(false);
    }
  };

  const handleDeletePost = async () => {
    if (!post?.id) return;

    setDeleteLoading(true);
    try {
      console.log(`Attempting to delete post ${post.id}`);
      await deletePost(post.id);
      console.log("Post deleted successfully");
      setShowDeleteConfirm(false);
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error("Delete error:", err);
      console.error("Status:", err?.response?.status);
      console.error("Response:", err?.response?.data);
      const errorMsg = err?.response?.data?.detail || err?.message || "Failed to delete post";
      setCartError(errorMsg);
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div className="post-card">
      {/* Header */}
      <div className="post-header">
        <div className="post-author-info">
          <div className="post-avatar">{post?.author_name?.charAt(0) || "F"}</div>
          <div className="post-author-details">
            <div className="post-author-name">{post?.author_name || "Farmer"}</div>
            <div className="post-timestamp">{new Date(post?.created_at).toLocaleDateString()}</div>
          </div>
        </div>
        {post?.price && (
          <div className="post-price">₱{post.price}</div>
        )}
      </div>

      {/* Title */}
      <h3 className="post-title">{post?.title}</h3>

      {/* Content */}
      <p className="post-content">{post?.content}</p>

      {/* Quantity Info */}
      {post?.quantity && (
        <div className="post-quantity-info">
          Available: {post.quantity} {post.unit === 'KG' ? 'kg' : 'g'}
        </div>
      )}

      {/* Image placeholder */}
      {post?.image && (
        <div className="post-image-placeholder">
          <img src={post.image} alt={post.title} className="post-image" />
        </div>
      )}

      {/* Footer Actions */}
      <div className="post-footer">
        <div className="post-actions">
          <button
            className="action-btn comment-btn"
            onClick={() => setShowComments(!showComments)}
          >
            💬 Comment
          </button>
          {canAddToCart && (
            <>
              {!showQuantitySelector ? (
                <button
                  className="action-btn cart-btn"
                  onClick={() => setShowQuantitySelector(true)}
                  disabled={cartLoading}
                >
                  🛒 Add to Cart
                </button>
              ) : (
                <div className="quantity-selector">
                  <input
                    type="number"
                    value={selectedQuantity}
                    onChange={(e) => setSelectedQuantity(e.target.value)}
                    placeholder={`Enter amount (${post.unit === 'KG' ? 'kg' : 'g'})`}
                    step="0.01"
                    min="0"
                    max={post.quantity}
                    className="quantity-input"
                  />
                  <button
                    className="action-btn add-btn"
                    onClick={handleAddToCart}
                    disabled={cartLoading}
                  >
                    {cartLoading ? "Adding..." : "Add"}
                  </button>
                  <button
                    className="action-btn cancel-btn"
                    onClick={() => {
                      setShowQuantitySelector(false);
                      setSelectedQuantity("");
                    }}
                  >
                    Cancel
                  </button>
                </div>
              )}
            </>
          )}
          {isOwner && (
            <button
              className="action-btn delete-btn"
              onClick={() => setShowDeleteConfirm(true)}
              disabled={deleteLoading}
              title="Delete this post"
            >
              🗑️ Delete
            </button>
          )}
        </div>
        {cartError && (
          <div className={`cart-message ${cartError.includes("✓") ? "success" : "error"}`}>
            {cartError}
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="delete-confirmation">
          <div className="confirmation-content">
            <p>Are you sure you want to delete this post?</p>
            <div className="confirmation-actions">
              <button
                className="confirm-btn delete"
                onClick={handleDeletePost}
                disabled={deleteLoading}
              >
                {deleteLoading ? "Deleting..." : "Delete"}
              </button>
              <button
                className="confirm-btn cancel"
                onClick={() => setShowDeleteConfirm(false)}
                disabled={deleteLoading}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Comments Section */}
      {showComments && (
        <CommentsSection postId={post?.id} user={user} onRefresh={onRefresh} />
      )}
    </div>
  );
}
