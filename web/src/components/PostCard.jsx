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

  const isOwner = user?.id === post?.author_id;
  const canAddToCart = post?.price && !isOwner;

  const handleAddToCart = async () => {
    if (!post?.id) return;
    
    setCartLoading(true);
    setCartError("");
    
    try {
      const { addToCart } = await import("../api/cart");
      await addToCart(post.id, 1);
      setCartError("✓ Added to cart");
      setTimeout(() => setCartError(""), 2000);
    } catch (err) {
      setCartError("Failed to add to cart");
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
          <div className="post-price">${post.price}</div>
        )}
      </div>

      {/* Title */}
      <h3 className="post-title">{post?.title}</h3>

      {/* Content */}
      <p className="post-content">{post?.content}</p>

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
            <button
              className="action-btn cart-btn"
              onClick={handleAddToCart}
              disabled={cartLoading}
            >
              {cartLoading ? "Adding..." : "🛒 Add to Cart"}
            </button>
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
