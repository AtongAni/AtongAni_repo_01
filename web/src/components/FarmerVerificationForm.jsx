import { useState, useEffect } from "react";
import { api } from "../api/client";
import "./FarmerVerificationForm.css";

export default function FarmerVerificationForm({ onVerificationSubmitted, onCancel }) {
  const [formData, setFormData] = useState({
    land_size: "",
    land_size_unit: "hectares",
    crop_type: "",
    previous_harvest_quantity: "",
    previous_harvest_unit: "KG",
    previous_harvest_date: "",
    farming_experience_years: "",
    location: "",
    notes: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [checkingEligibility, setCheckingEligibility] = useState(true);
  const [canApply, setCanApply] = useState(false);
  const [existingProfile, setExistingProfile] = useState(null);

  // Check if farmer can apply for verification
  useEffect(() => {
    async function checkEligibility() {
      try {
        const response = await api.get("/api/farmer-harvest-profile/my_profile/");
        const profile = response.data;
        setExistingProfile(profile);
        
        // Can apply if no profile or if previous was rejected/revision requested
        const canReapply = ['REJECTED', 'REVISION_REQUESTED'].includes(profile.status);
        setCanApply(canReapply);
        
        if (!canReapply) {
          setError(`You already have an active profile with status: ${profile.status}. You can only submit a new application if your previous one was rejected or revision is requested.`);
        }
      } catch (err) {
        // 404 means no profile exists - farmer can apply
        if (err?.response?.status === 404) {
          setCanApply(true);
        } else {
          console.error("Error checking eligibility:", err);
          // Allow to proceed if we can't check
          setCanApply(true);
        }
      } finally {
        setCheckingEligibility(false);
      }
    }
    
    checkEligibility();
  }, []);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!formData.land_size.trim()) {
      setError("Land size is required");
      return;
    }
    if (!formData.crop_type.trim()) {
      setError("Crop type is required");
      return;
    }

    setLoading(true);

    try {
      const payload = {
        land_size: parseFloat(formData.land_size),
        land_size_unit: formData.land_size_unit,
        crop_type: formData.crop_type.trim(),
        previous_harvest_quantity: formData.previous_harvest_quantity?.trim()
          ? parseFloat(formData.previous_harvest_quantity)
          : null,
        previous_harvest_unit: formData.previous_harvest_unit,
        previous_harvest_date: formData.previous_harvest_date?.trim() ? formData.previous_harvest_date : null,
        farming_experience_years: formData.farming_experience_years?.trim()
          ? parseInt(formData.farming_experience_years)
          : null,
        location: formData.location?.trim() || "",
        notes: formData.notes?.trim() || "",
      };

      console.log("Submitting payload:", payload);
      const response = await api.post("/api/farmer-harvest-profile/", payload);

      setSuccess(
        "Your harvest forecasting profile has been submitted for review! Our team will verify your information and approve your access."
      );

      // Reset form
      setFormData({
        land_size: "",
        land_size_unit: "hectares",
        crop_type: "",
        previous_harvest_quantity: "",
        previous_harvest_unit: "KG",
        previous_harvest_date: "",
        farming_experience_years: "",
        location: "",
        notes: "",
      });

      setTimeout(() => {
        setSuccess("");
        if (onVerificationSubmitted) onVerificationSubmitted();
      }, 2500);
    } catch (err) {
      console.error("Verification submission error:", err);
      console.error("Error response data:", err?.response?.data);

      let errorMsg = "Failed to submit verification data";

      if (err?.response?.status === 400) {
        if (err.response.data?.non_field_errors?.[0]) {
          errorMsg = err.response.data.non_field_errors[0];
        } else if (err.response.data?.detail) {
          errorMsg = err.response.data.detail;
        } else {
          const errors = Object.entries(err.response.data)
            .map(
              ([field, msgs]) => {
                const msgText = Array.isArray(msgs) ? msgs[0] : msgs;
                return `${field}: ${msgText}`;
              }
            )
            .join("; ");
          errorMsg = errors || errorMsg;
        }
      } else if (err?.response?.status === 409) {
        errorMsg = "You already have a harvest forecasting profile. You cannot create another one.";
      } else if (err?.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      } else if (err?.message) {
        errorMsg = err.message;
      }

      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="farmer-verification-form">
      <h3>🚜 Apply for Harvest Forecasting</h3>
      <p className="form-intro">
        Please provide details about your farm and farming history. Our team will review and
        verify your information to grant access to the harvest forecasting feature.
      </p>

      {checkingEligibility ? (
        <div className="loading-message">Checking your eligibility...</div>
      ) : !canApply ? (
        <div className="form-error" style={{ fontSize: '1rem', padding: '15px', marginBottom: '20px' }}>
          <strong>❌ Unable to Apply</strong>
          <p>{error}</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="verification-form">
        <div className="form-section">
          <h4>Farm Information</h4>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="land_size">
                Land Size *
              </label>
              <input
                id="land_size"
                type="number"
                name="land_size"
                value={formData.land_size}
                onChange={handleChange}
                placeholder="e.g., 2.5"
                step="0.01"
                min="0"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="land_size_unit">Unit</label>
              <select
                id="land_size_unit"
                name="land_size_unit"
                value={formData.land_size_unit}
                onChange={handleChange}
                className="form-input"
              >
                <option value="hectares">Hectares (ha)</option>
                <option value="acres">Acres</option>
                <option value="square_meters">Square Meters (m²)</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="crop_type">
              Main Crop Type(s) *
            </label>
            <input
              id="crop_type"
              type="text"
              name="crop_type"
              value={formData.crop_type}
              onChange={handleChange}
              placeholder="e.g., Tomatoes, Rice, Corn"
              maxLength={255}
              className="form-input"
            />
            <small>List all crops you grow separated by commas</small>
          </div>

          <div className="form-group">
            <label htmlFor="location">Farm Location</label>
            <input
              id="location"
              type="text"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g., Bulacan, Philippines"
              maxLength={255}
              className="form-input"
            />
          </div>
        </div>

        <div className="form-section">
          <h4>Farming Experience</h4>

          <div className="form-group">
            <label htmlFor="farming_experience_years">
              Years of Farming Experience
            </label>
            <input
              id="farming_experience_years"
              type="number"
              name="farming_experience_years"
              value={formData.farming_experience_years}
              onChange={handleChange}
              placeholder="e.g., 10"
              min="0"
              max="100"
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="notes">Additional Notes</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Any additional information about your farming practices, certifications, irrigation methods, etc..."
              rows={3}
              maxLength={500}
              className="form-textarea"
            />
            <span className="char-count">{formData.notes.length}/500</span>
          </div>
        </div>

        <div className="form-section">
          <h4>Previous Harvest (Optional)</h4>
          <p className="section-help">
            Providing previous harvest data helps us give more accurate forecasts
          </p>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="previous_harvest_quantity">
                Previous Harvest Quantity
              </label>
              <input
                id="previous_harvest_quantity"
                type="number"
                name="previous_harvest_quantity"
                value={formData.previous_harvest_quantity}
                onChange={handleChange}
                placeholder="e.g., 500"
                step="0.01"
                min="0"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="previous_harvest_unit">Unit</label>
              <select
                id="previous_harvest_unit"
                name="previous_harvest_unit"
                value={formData.previous_harvest_unit}
                onChange={handleChange}
                className="form-input"
              >
                <option value="KG">Kilogram (kg)</option>
                <option value="G">Gram (g)</option>
                <option value="TON">Metric Ton</option>
                <option value="BAGS">Bags</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="previous_harvest_date">
              Previous Harvest Date
            </label>
            <input
              id="previous_harvest_date"
              type="date"
              name="previous_harvest_date"
              value={formData.previous_harvest_date}
              onChange={handleChange}
              className="form-input"
            />
          </div>
        </div>

        {error && <div className="form-error">{error}</div>}
        {success && <div className="form-success">{success}</div>}

        <div className="form-actions">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="btn-back"
            >
              ← Back
            </button>
          )}
          <button
            type="submit"
            disabled={loading}
            className="submit-btn"
          >
            {loading ? "Submitting..." : "Submit for Verification"}
          </button>
        </div>
      </form>
      )}

      <div className="info-box">
        <h5>📋 What happens next?</h5>
        <ul>
          <li>Your application will be reviewed by our team</li>
          <li>We'll verify your farm information against official records</li>
          <li>You'll receive approval notification via email</li>
          <li>Once approved, you can start creating harvest forecasts</li>
        </ul>
      </div>
    </div>
  );
}
