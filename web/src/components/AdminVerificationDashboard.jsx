import { useState, useEffect } from "react";
import { api } from "../api/client";
import "./AdminVerificationDashboard.css";

export default function AdminVerificationDashboard() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [selectedApp, setSelectedApp] = useState(null);
  const [actionType, setActionType] = useState(null); // "approve", "reject", "revise"
  const [notes, setNotes] = useState("");

  useEffect(() => {
    loadPendingApplications();
  }, []);

  async function loadPendingApplications() {
    setLoading(true);
    setError("");
    try {
      const response = await api.get("/api/farmer-harvest-profile/pending_reviews/");
      setApplications(response.data.profiles || []);
    } catch (err) {
      console.error("Error loading applications:", err);
      setError("Failed to load pending applications");
    } finally {
      setLoading(false);
    }
  }

  async function handleAction(profileId, action, message) {
    setActionLoading(profileId);
    setError("");
    setSuccess("");

    // Validate message is provided for all actions
    if (!message || !message.trim()) {
      setError(`Please provide ${action === 'approve' ? 'approval' : action === 'reject' ? 'rejection' : 'revision'} notes`);
      setActionLoading(null);
      return;
    }

    try {
      let endpoint = `/api/farmer-harvest-profile/${profileId}/`;
      let payload = { admin_notes: message };

      if (action === "approve") {
        endpoint += "approve/";
      } else if (action === "reject") {
        endpoint += "reject/";
      } else if (action === "revise") {
        endpoint += "request_revision/";
      }

      const response = await api.post(endpoint, payload);

      setSuccess(response.data.message);
      
      // Remove the application from the list
      setApplications(applications.filter(app => app.id !== profileId));
      
      // Reset form
      setSelectedApp(null);
      setActionType(null);
      setNotes("");

      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      console.error("Error performing action:", err);
      let errorMsg = "Failed to perform action";
      if (err?.response?.data?.error) {
        errorMsg = err.response.data.error;
      } else if (err?.response?.data?.message) {
        errorMsg = err.response.data.message;
      }
      setError(errorMsg);
    } finally {
      setActionLoading(null);
    }
  }

  function openActionDialog(app, action) {
    setSelectedApp(app);
    setActionType(action);
    setNotes("");
  }

  function closeActionDialog() {
    setSelectedApp(null);
    setActionType(null);
    setNotes("");
  }

  if (loading) {
    return (
      <div className="admin-verification-dashboard">
        <div className="loading">Loading pending applications...</div>
      </div>
    );
  }

  return (
    <div className="admin-verification-dashboard">
      <div className="dashboard-header">
        <h2>📋 Farmer Verification Applications</h2>
        <div className="header-stats">
          <div className="stat">
            <span className="stat-number">{applications.length}</span>
            <span className="stat-label">Pending Review</span>
          </div>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button className="alert-close" onClick={() => setError("")}>×</button>
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
          <button className="alert-close" onClick={() => setSuccess("")}>×</button>
        </div>
      )}

      {applications.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">✓</div>
          <h3>All caught up!</h3>
          <p>No pending farmer applications to review.</p>
        </div>
      ) : (
        <div className="applications-list">
          {applications.map((app) => (
            <div key={app.id} className="application-card">
              <div className="app-header">
                <div className="farmer-info">
                  <h3>{app.farmer_name}</h3>
                  <p className="submission-date">
                    Submitted: {new Date(app.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="status-badge pending">Pending Review</div>
              </div>

              <div className="app-details">
                <div className="detail-row">
                  <span className="detail-label">Crop Type:</span>
                  <span className="detail-value">{app.crop_type}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Land Size:</span>
                  <span className="detail-value">
                    {app.land_size} {app.land_size_unit}
                  </span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Location:</span>
                  <span className="detail-value">{app.location || "Not provided"}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Experience:</span>
                  <span className="detail-value">
                    {app.farming_experience_years ? `${app.farming_experience_years} years` : "Not provided"}
                  </span>
                </div>

                {app.previous_harvest_date && (
                  <div className="detail-row">
                    <span className="detail-label">Previous Harvest:</span>
                    <span className="detail-value">
                      {app.previous_harvest_quantity} {app.previous_harvest_unit} on{" "}
                      {new Date(app.previous_harvest_date).toLocaleDateString()}
                    </span>
                  </div>
                )}

                {app.notes && (
                  <div className="detail-section">
                    <span className="detail-label">Notes:</span>
                    <p className="detail-notes">{app.notes}</p>
                  </div>
                )}
              </div>

              <div className="app-actions">
                <button
                  className="btn btn-approve"
                  onClick={() => openActionDialog(app, "approve")}
                  disabled={actionLoading === app.id}
                >
                  ✓ Approve
                </button>
                <button
                  className="btn btn-revise"
                  onClick={() => openActionDialog(app, "revise")}
                  disabled={actionLoading === app.id}
                >
                  ✎ Request Revision
                </button>
                <button
                  className="btn btn-reject"
                  onClick={() => openActionDialog(app, "reject")}
                  disabled={actionLoading === app.id}
                >
                  ✕ Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Action Confirmation Dialog */}
      {selectedApp && actionType && (
        <div className="modal-overlay" onClick={closeActionDialog}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                {actionType === "approve"
                  ? "✓ Approve Farmer"
                  : actionType === "reject"
                  ? "✕ Reject Application"
                  : "✎ Request Revision"}
              </h3>
              <button className="modal-close" onClick={closeActionDialog}>×</button>
            </div>

            <div className="modal-body">
              <p className="farmer-name">Farmer: <strong>{selectedApp.farmer_name}</strong></p>

              {actionType === "approve" && (
                <div className="action-info">
                  <p>✓ This farmer will be approved to use the harvest forecasting feature.</p>
                </div>
              )}

              {actionType === "reject" && (
                <div className="action-info warning">
                  <p>✕ This will reject the farmer's application. Please provide a clear reason.</p>
                </div>
              )}

              {actionType === "revise" && (
                <div className="action-info">
                  <p>✎ The farmer will be notified that their application needs revision.</p>
                </div>
              )}

              <div className="form-group">
                <label htmlFor="action-notes">
                  {actionType === "revise" ? "📝 Revision Feedback *" : "Admin Notes"}
                  {(actionType === "reject" || actionType === "revise") && <span className="required">*</span>}
                </label>
                <textarea
                  id="action-notes"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder={
                    actionType === "revise"
                      ? "Specify what needs to be revised (farmer will see this)..."
                      : actionType === "reject"
                      ? "Explain why the application is rejected (farmer will see this)..."
                      : "Optional notes..."
                  }
                  rows={4}
                  maxLength={500}
                />
                <span className="char-count">{notes.length}/500</span>
              </div>
            </div>

            <div className="modal-footer">
              <button
                className="btn btn-secondary"
                onClick={closeActionDialog}
                disabled={actionLoading === selectedApp.id}
              >
                Cancel
              </button>
              <button
                className={`btn btn-${
                  actionType === "approve"
                    ? "approve"
                    : actionType === "revise"
                    ? "revise"
                    : "reject"
                }`}
                onClick={() =>
                  handleAction(
                    selectedApp.id,
                    actionType,
                    notes
                  )
                }
                disabled={
                  actionLoading === selectedApp.id ||
                  ((actionType === "reject" || actionType === "revise") && !notes.trim())
                }
              >
                {actionLoading === selectedApp.id ? "Processing..." : "Confirm"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
