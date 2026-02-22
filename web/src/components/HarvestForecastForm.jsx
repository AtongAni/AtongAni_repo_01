import { useState, useEffect } from "react";
import { createPost, uploadPostImages } from "../api/posts";
import { api } from "../api/client";
import FarmerVerificationForm from "./FarmerVerificationForm";
import "./FarmerPostForm.css";

export default function HarvestForecastForm({ onPostCreated }) {
  // Verification state
  const [isVerified, setIsVerified] = useState(null);
  const [verificationLoading, setVerificationLoading] = useState(true);
  const [showVerificationForm, setShowVerificationForm] = useState(false);
  const [verificationStatus, setVerificationStatus] = useState(null);
  const [verificationMessage, setVerificationMessage] = useState("");
  const [adminNotes, setAdminNotes] = useState("");

  // Form state
  const [title, setTitle] = useState("");
  const [cropName, setCropName] = useState("");
  const [content, setContent] = useState("");
  const [expectedHarvestDate, setExpectedHarvestDate] = useState("");
  const [expectedQuantity, setExpectedQuantity] = useState("");
  const [unit, setUnit] = useState("KG");
  const [growthStage, setGrowthStage] = useState("Seedling");
  const [environmentalConditions, setEnvironmentalConditions] = useState("");
  const [images, setImages] = useState([]);
  const [createdPostId, setCreatedPostId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Check verification status on mount
  useEffect(() => {
    checkVerificationStatus();
  }, []);

  async function checkVerificationStatus() {
    try {
      const response = await api.get("/api/farmer-harvest-profile/my_profile/");
      const profile = response.data;
      const isApproved = profile.status === 'APPROVED';
      setIsVerified(isApproved);
      setVerificationStatus(profile.status);
      setAdminNotes(profile.admin_notes || "");
      
      // Set appropriate message based on status
      if (profile.status === 'PENDING') {
        setVerificationMessage("⏳ Your verification application is being reviewed. Please check back soon.");
      } else if (profile.status === 'REVISION_REQUESTED') {
        setVerificationMessage(`📝 Revision Requested: ${profile.admin_notes}`);
      } else if (profile.status === 'REJECTED') {
        setVerificationMessage(`❌ Your application was rejected. Reason: ${profile.admin_notes}`);
      }
    } catch (err) {
      if (err?.response?.status === 404) {
        // No profile exists yet - this is expected for first-time users
        setIsVerified(false);
        setVerificationStatus(null);
      } else {
        console.error("Error checking verification status:", err);
        setIsVerified(false);
      }
    } finally {
      setVerificationLoading(false);
    }
  }

  function handleVerificationSubmitted() {
    setShowVerificationForm(false);
    // Re-check verification status
    checkVerificationStatus();
  }

  function handleImagesChange(e) {
    const files = Array.from(e.target.files);
    
    // Check total will not exceed 15
    const totalImages = images.length + files.length;
    if (totalImages > 15) {
      setError(`Maximum 15 images allowed. You have ${images.length}, trying to add ${files.length}.`);
      return;
    }

    const newImages = [];
    
    for (const file of files) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError(`"${file.name}" is too large (max 5MB).`);
        continue;
      }
      
      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
      if (!allowedTypes.includes(file.type)) {
        setError(`"${file.name}" has unsupported format. Allowed: JPEG, PNG, GIF, WebP.`);
        continue;
      }

      // Create image object with unique ID for removal
      const imageId = `${Date.now()}-${Math.random()}`;
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImages(prev => [...prev, {
          id: imageId,
          file: file,
          preview: reader.result,
          uploaded: false
        }]);
      };
      reader.readAsDataURL(file);
    }

    setError("");
  }

  function removeImage(imageId) {
    setImages(images.filter(img => img.id !== imageId));
  }

  async function uploadImages(postId) {
    if (images.length === 0) return;
    
    setUploading(true);
    try {
      const filesToUpload = images.filter(img => !img.uploaded).map(img => img.file);
      
      if (filesToUpload.length === 0) {
        return;
      }

      await uploadPostImages(postId, filesToUpload);
      
      // Mark images as uploaded
      setImages(images.map(img => ({ ...img, uploaded: true })));
    } catch (err) {
      console.error("Image upload error:", err);
      throw err;
    } finally {
      setUploading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    if (!cropName.trim()) {
      setError("Crop/Product name is required");
      return;
    }
    if (!content.trim()) {
      setError("Description/Notes are required");
      return;
    }
    if (!expectedHarvestDate) {
      setError("Expected harvest date is required");
      return;
    }

    setLoading(true);

    try {
      // Create the post
      const formData = new FormData();
      formData.append('title', title.trim());
      formData.append('content', content.trim());
      formData.append('post_type', 'HARVEST_FORECAST');
      
      // Store additional harvest forecast data in price field (as JSON-like string) or create new fields
      // For now, we'll use existing fields creatively
      if (cropName) {
        formData.append('quantity', expectedQuantity || 0);
      }
      
      if (unit) {
        formData.append('unit', unit);
      }

      const postResponse = await createPost(formData);
      const postId = postResponse.data.id;
      setCreatedPostId(postId);

      // Upload images if any
      if (images.length > 0) {
        setUploading(true);
        try {
          await uploadImages(postId);
        } catch (err) {
          console.error("Image upload error:", err);
          setError("Forecast created but image upload failed. You can try uploading images later.");
          throw err;
        } finally {
          setUploading(false);
        }
      }

      setSuccess("Harvest forecast posted successfully!");
      setTitle("");
      setCropName("");
      setContent("");
      setExpectedHarvestDate("");
      setExpectedQuantity("");
      setUnit("KG");
      setGrowthStage("Seedling");
      setEnvironmentalConditions("");
      setImages([]);
      setCreatedPostId(null);

      setTimeout(() => {
        setSuccess("");
        if (onPostCreated) onPostCreated();
      }, 1500);
    } catch (err) {
      console.error("Harvest forecast creation error:", err);
      
      let errorMsg = "Failed to create harvest forecast";
      
      if (err?.response?.status === 500) {
        errorMsg = "Server error - please contact support or check backend logs";
      } else if (err?.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      } else if (err?.response?.data?.non_field_errors?.[0]) {
        errorMsg = err.response.data.non_field_errors[0];
      } else if (err?.response?.data) {
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
      {/* Show loading state while checking verification */}
      {verificationLoading && (
        <div style={{ textAlign: "center", padding: "20px" }}>
          <p style={{ color: "#666" }}>Checking verification status...</p>
        </div>
      )}

      {/* Show verification status messages if not verified */}
      {!verificationLoading && !isVerified && (
        <>
          {verificationStatus === 'PENDING' && (
            <div className="verification-status-box in-process">
              <h3>⏳ Application In Process</h3>
              <p>Your harvest forecasting feature application is being reviewed by our team.</p>
              <p style={{ fontSize: '14px', color: '#555', marginTop: '8px' }}>Please check back soon for updates.</p>
            </div>
          )}

          {verificationStatus === 'REVISION_REQUESTED' && (
            <div className="verification-status-box revision-requested">
              <h3>📝 Revision Requested</h3>
              <p>Our team has requested some changes to your application:</p>
              <div className="admin-notes-box">
                <p style={{ fontStyle: 'italic', marginTop: '8px' }}>{adminNotes}</p>
              </div>
              <button
                type="button"
                onClick={() => setShowVerificationForm(true)}
                className="btn-avail-feature"
              >
                ✏️ Revise Application
              </button>
            </div>
          )}

          {verificationStatus === 'REJECTED' && (
            <div className="verification-status-box rejected">
              <h3>❌ Application Rejected</h3>
              <p>Unfortunately, your application could not be approved at this time:</p>
              <div className="admin-notes-box">
                <p style={{ fontStyle: 'italic', marginTop: '8px' }}>{adminNotes}</p>
              </div>
              <p style={{ fontSize: '14px', color: '#666', marginTop: '12px' }}>
                You can submit a new application addressing the feedback above.
              </p>
              <button
                type="button"
                onClick={() => setShowVerificationForm(true)}
                className="btn-avail-feature"
              >
                ✓ Submit New Application
              </button>
            </div>
          )}

          {!verificationStatus && !showVerificationForm && (
            <div className="verification-required-box">
              <div className="verification-required-content">
                <h3>🔐 Verification Required</h3>
                <p>
                  To access the Harvest Forecasting feature, we need to verify your farm
                  information first. This helps us provide accurate forecasts and maintain the
                  quality of our platform.
                </p>
                <button
                  type="button"
                  onClick={() => setShowVerificationForm(true)}
                  className="btn-avail-feature"
                >
                  ✓ Avail Feature Now
                </button>
              </div>
            </div>
          )}

          {showVerificationForm && (
            <FarmerVerificationForm 
              onVerificationSubmitted={handleVerificationSubmitted}
              onCancel={() => setShowVerificationForm(false)}
            />
          )}
        </>
      )}

      {/* Show the actual form only if verified */}
      {!verificationLoading && isVerified && (
        <>
          <h3>Create Harvest Forecast</h3>
          <p style={{ fontSize: '14px', color: '#666', marginBottom: '16px' }}>
            Share your harvest forecast to help the community plan ahead
          </p>

          <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="title">Forecast Title *</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g., Tomato Harvest 2026"
            maxLength={100}
            className="form-input"
          />
          <span className="char-count">{title.length}/100</span>
        </div>

        <div className="form-group">
          <label htmlFor="cropName">Crop/Product Name *</label>
          <input
            id="cropName"
            type="text"
            value={cropName}
            onChange={(e) => setCropName(e.target.value)}
            placeholder="e.g., Heirloom Tomatoes"
            maxLength={100}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="expectedHarvestDate">Expected Harvest Date *</label>
          <input
            id="expectedHarvestDate"
            type="date"
            value={expectedHarvestDate}
            onChange={(e) => setExpectedHarvestDate(e.target.value)}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="growthStage">Current Growth Stage</label>
          <select
            id="growthStage"
            value={growthStage}
            onChange={(e) => setGrowthStage(e.target.value)}
            className="form-input"
          >
            <option value="Seedling">Seedling</option>
            <option value="Vegetative">Vegetative</option>
            <option value="Flowering">Flowering</option>
            <option value="Fruiting">Fruiting</option>
            <option value="Mature">Mature</option>
            <option value="Ready for Harvest">Ready for Harvest</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="expectedQuantity">Expected Quantity/Yield</label>
            <input
              id="expectedQuantity"
              type="number"
              value={expectedQuantity}
              onChange={(e) => setExpectedQuantity(e.target.value)}
              placeholder="Enter expected quantity"
              step="0.01"
              min="0"
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="unit">Unit of Measurement</label>
            <select
              id="unit"
              value={unit}
              onChange={(e) => setUnit(e.target.value)}
              className="form-input"
            >
              <option value="KG">Kilogram (kg)</option>
              <option value="G">Gram (g)</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="environmentalConditions">Environmental Conditions</label>
          <textarea
            id="environmentalConditions"
            value={environmentalConditions}
            onChange={(e) => setEnvironmentalConditions(e.target.value)}
            placeholder="Describe current weather, soil conditions, irrigation status, etc..."
            rows={3}
            maxLength={500}
            className="form-textarea"
          />
          <span className="char-count">{environmentalConditions.length}/500</span>
        </div>

        <div className="form-group">
          <label htmlFor="content">Description & Notes *</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Add detailed notes about your harvest forecast, any concerns, expected quality, pest management, etc..."
            rows={4}
            maxLength={1000}
            className="form-textarea"
          />
          <span className="char-count">{content.length}/1000</span>
        </div>

        <div className="form-group">
          <label htmlFor="images">Field/Crop Images (max 15)</label>
          <div className="image-upload-section">
            <input
              id="images"
              type="file"
              multiple
              accept="image/jpeg,image/png,image/gif,image/webp"
              onChange={handleImagesChange}
              className="form-input"
              disabled={images.length >= 15}
            />
            <p className="image-help-text">
              Supported formats: JPEG, PNG, GIF, WebP (max 5MB each)
              <br />
              {images.length}/15 images selected
            </p>
            
            {images.length > 0 && (
              <div className="image-preview-grid">
                {images.map((img) => (
                  <div key={img.id} className="image-preview-item">
                    <img src={img.preview} alt="Preview" className="image-preview" />
                    <button
                      type="button"
                      onClick={() => removeImage(img.id)}
                      className="remove-image-btn"
                      disabled={uploading}
                    >
                      ✕
                    </button>
                    {img.uploaded && <div className="uploaded-badge">✓</div>}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {error && <div className="form-error">{error}</div>}
        {success && <div className="form-success">{success}</div>}

        <button
          type="submit"
          disabled={loading || uploading}
          className="submit-btn"
        >
          {loading ? "Creating forecast..." : uploading ? "Uploading images..." : "Post Forecast"}
        </button>
      </form>
        </>
      )}
    </div>
  );
}
