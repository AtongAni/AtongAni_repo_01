import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { me } from "../api/auth";
import { setAuthToken, clearAuthToken } from "../api/client";
import PostFeed from "../components/PostFeed";
import FarmerPostForm from "../components/FarmerPostForm";
import FarmerOrdersManagement from "../components/FarmerOrdersManagement";
import OrdersView from "../components/OrdersView";
import CartView from "../components/CartView";
import AdminDashboard from "../components/AdminDashboard";
import RiderDashboard from "../components/RiderDashboard";
import "./Dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState("Loading...");
  const [activeTab, setActiveTab] = useState("feed");
  const [refreshFeed, setRefreshFeed] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      setAuthToken(token);
      me()
        .then((res) => {
          setUser(res.data);
          setStatus("");
        })
        .catch((err) => {
          console.log(err);
          clearAuthToken();
          setUser(null);
          setStatus("");
        });
    } else {
      setStatus("");
    }
  }, []);

  function handleLogout() {
    clearAuthToken();
    navigate("/");
  }

  function handlePostCreated() {
    setRefreshFeed((prev) => prev + 1);
    setActiveTab("feed");
  }

  if (status) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <span>{status}</span>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Enhanced Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="brand-section">
            <div className="brand-icon">🌱</div>
            <h1 className="brand-title">AtongAni</h1>
          </div>
          
          {user ? (
            <div className="header-user">
              <div className="user-avatar">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <div className="user-info">
                <p className="user-name">{user.username}</p>
                <p className="user-role">
                  {user.role === "FARMER" ? "🚜 Farmer" : 
                   user.role === "RIDER" ? "🏍️ Rider" : 
                   user.role === "ADMIN" ? "👑 Admin" : "👤 Customer"}
                </p>
              </div>
            </div>
          ) : (
            <div className="header-actions">
              <button 
                className="login-header-btn" 
                onClick={() => navigate("/login")}
              >
                <span className="btn-text">Login / Sign Up</span>
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Enhanced Tabs Navigation */}
      <nav className="dashboard-tabs">
        <div className="tabs-container">
          <button
            className={`tab-btn ${activeTab === "feed" ? "active" : ""}`}
            onClick={() => setActiveTab("feed")}
            title="Browse all posts"
          >
            <span className="tab-icon">📱</span>
            <span className="tab-label">Feed</span>
          </button>

          {user?.role === "FARMER" && (
            <>
              <button
                className={`tab-btn ${activeTab === "myPosts" ? "active" : ""}`}
                onClick={() => setActiveTab("myPosts")}
                title="Manage your posts"
              >
                <span className="tab-icon">📝</span>
                <span className="tab-label">My Posts</span>
              </button>
              <button
                className={`tab-btn ${activeTab === "orders" ? "active" : ""}`}
                onClick={() => setActiveTab("orders")}
                title="Manage customer orders"
              >
                <span className="tab-icon">📦</span>
                <span className="tab-label">Orders</span>
              </button>
            </>
          )}

          {user && (
            <button
              className={`tab-btn ${activeTab === "cart" ? "active" : ""}`}
              onClick={() => setActiveTab("cart")}
              title="View shopping cart"
            >
              <span className="tab-icon">🛒</span>
              <span className="tab-label">Cart</span>
            </button>
          )}

          {user?.role === "CUSTOMER" && (
            <button
              className={`tab-btn ${activeTab === "orders" ? "active" : ""}`}
              onClick={() => setActiveTab("orders")}
              title="View your orders"
            >
              <span className="tab-icon">📋</span>
              <span className="tab-label">My Orders</span>
            </button>
          )}

          {user?.role === "RIDER" && (
            <button
              className={`tab-btn ${activeTab === "deliveries" ? "active" : ""}`}
              onClick={() => setActiveTab("deliveries")}
              title="Manage deliveries"
            >
              <span className="tab-icon">🚚</span>
              <span className="tab-label">Deliveries</span>
            </button>
          )}

          {user?.role === "ADMIN" && (
            <button
              className={`tab-btn ${activeTab === "admin" ? "active" : ""}`}
              onClick={() => setActiveTab("admin")}
              title="Admin dashboard"
            >
              <span className="tab-icon">⚙️</span>
              <span className="tab-label">Admin</span>
            </button>
          )}

          {user && (
            <button
              className={`tab-btn ${activeTab === "profile" ? "active" : ""}`}
              onClick={() => setActiveTab("profile")}
              title="Account settings"
            >
              <span className="tab-icon">👤</span>
              <span className="tab-label">Profile</span>
            </button>
          )}
        </div>
      </nav>

      {/* Enhanced Tab Content */}
      <main className="dashboard-content">
        {activeTab === "feed" && (
          <div className="tab-content-wrapper">
            <PostFeed user={user} refreshTrigger={refreshFeed} />
          </div>
        )}

        {activeTab === "myPosts" && user?.role === "FARMER" && (
          <div className="tab-content-wrapper">
            <div className="section-header">
              <h2>Manage Your Posts</h2>
              <p>Create and manage your agricultural listings</p>
            </div>
            <FarmerPostForm onPostCreated={handlePostCreated} />
            <PostFeed user={user} refreshTrigger={refreshFeed} />
          </div>
        )}

        {activeTab === "orders" && user?.role === "FARMER" && (
          <div className="tab-content-wrapper">
            <div className="section-header">
              <h2>Order Management</h2>
              <p>Track and manage customer orders</p>
            </div>
            <FarmerOrdersManagement />
          </div>
        )}

        {activeTab === "cart" && user && (
          <div className="tab-content-wrapper">
            <div className="section-header">
              <h2>Shopping Cart</h2>
              <p>Review your selected items</p>
            </div>
            <CartView />
          </div>
        )}

        {activeTab === "orders" && user?.role === "CUSTOMER" && (
          <div className="tab-content-wrapper">
            <div className="section-header">
              <h2>My Orders</h2>
              <p>Track your order history and status</p>
            </div>
            <OrdersView />
          </div>
        )}

        {activeTab === "deliveries" && user?.role === "RIDER" && (
          <div className="tab-content-wrapper">
            <div className="section-header">
              <h2>Delivery Management</h2>
              <p>Manage your delivery assignments</p>
            </div>
            <RiderDashboard />
          </div>
        )}

        {activeTab === "admin" && user?.role === "ADMIN" && (
          <div className="tab-content-wrapper">
            <div className="section-header">
              <h2>Admin Dashboard</h2>
              <p>System administration and management</p>
            </div>
            <AdminDashboard user={user} />
          </div>
        )}

        {activeTab === "profile" && user && (
          <div className="tab-content-wrapper">
            <div className="profile-view">
              <div className="profile-card">
                <div className="profile-header">
                  <div className="profile-avatar-large">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="profile-info">
                    <h2>{user.username}</h2>
                    <p className="profile-role">
                      {user.role === "FARMER" ? "🚜 Farmer" : 
                       user.role === "RIDER" ? "🏍️ Rider" : 
                       user.role === "ADMIN" ? "👑 Admin" : "👤 Customer"}
                    </p>
                  </div>
                </div>

                <div className="profile-details">
                  <div className="detail-item">
                    <div className="detail-icon">📧</div>
                    <div className="detail-content">
                      <span className="detail-label">Email</span>
                      <span className="detail-value">***{user.email}***</span>
                    </div>
                  </div>
                  <div className="detail-item">
                    <div className="detail-icon">🏷️</div>
                    <div className="detail-content">
                      <span className="detail-label">Account Type</span>
                      <span className="detail-value">
                        {user.role === "FARMER" ? "Farmer Account" : 
                         user.role === "RIDER" ? "Rider Account" : 
                         user.role === "ADMIN" ? "Admin Account" : "Customer Account"}
                      </span>
                    </div>
                  </div>
                  <div className="detail-item">
                    <div className="detail-icon">📅</div>
                    <div className="detail-content">
                      <span className="detail-label">Member Since</span>
                      <span className="detail-value">
                        {new Date(user.date_joined).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </span>
                    </div>
                  </div>
                </div>

                <button onClick={handleLogout} className="logout-btn">
                  <span className="btn-icon">🚪</span>
                  <span className="btn-text">Logout</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
