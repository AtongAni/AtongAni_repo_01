import { useState } from "react";
import { createPost } from "../api/posts";
import "./FarmerPostForm.css";

export default function FarmerPostForm({ onPostCreated }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [price, setPrice] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    if (!content.trim()) {
      setError("Description is required");
      return;
    }

    setLoading(true);

    try {
      const postData = {
        title: title.trim(),
        content: content.trim(),
      };

      if (price && !isNaN(price)) {
        postData.price = parseFloat(price);
      }

      await createPost(postData);
      setSuccess("Post created successfully!");
      setTitle("");
      setContent("");
      setPrice("");

      setTimeout(() => {
        setSuccess("");
        if (onPostCreated) onPostCreated();
      }, 1500);
    } catch (err) {
      console.error("Post creation error:", err);
      // Log the full error for debugging
      console.error("Response status:", err?.response?.status);
      console.error("Response data:", err?.response?.data);
      console.error("Error message:", err?.message);
      
      // Extract error message from various possible response formats
      let errorMsg = "Failed to create post";
      
      if (err?.response?.status === 500) {
        errorMsg = "Server error - please contact support or check backend logs";
      } else if (err?.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      } else if (err?.response?.data?.non_field_errors?.[0]) {
        errorMsg = err.response.data.non_field_errors[0];
      } else if (err?.response?.data) {
        // If there are field-specific errors, show them
        const errors = Object.entries(err.response.data)
          .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs[0] : msgs}`)
          .join(", ");
        errorMsg = errors || errorMsg;
      } else if (err?.message) {
        errorMsg = err.message;
      }
      
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="farmer-post-form">
      <h3>Create a New Post</h3>

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What are you selling?"
            maxLength={100}
            className="form-input"
          />
          <span className="char-count">{title.length}/100</span>
        </div>

        <div className="form-group">
          <label htmlFor="content">Description *</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Describe your product, quality, etc..."
            rows={4}
            maxLength={1000}
            className="form-textarea"
          />
          <span className="char-count">{content.length}/1000</span>
        </div>

        <div className="form-group">
          <label htmlFor="price">Price ($)</label>
          <input
            id="price"
            type="number"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            placeholder="Enter price (optional)"
            step="0.01"
            min="0"
            className="form-input"
          />
        </div>

        {error && <div className="form-error">{error}</div>}
        {success && <div className="form-success">{success}</div>}

        <button
          type="submit"
          disabled={loading}
          className="submit-btn"
        >
          {loading ? "Posting..." : "Post"}
        </button>
      </form>
    </div>
  );
}
