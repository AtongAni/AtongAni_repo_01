import React from "react";
import { useNavigate } from "react-router-dom";
import "../responsive.css"; 

function Welcome() {
  const navigate = useNavigate();

  const handleProceed = () => {
    navigate("/login");
  };

  return (
    <div className="welcome-page">
      
      <header className="navbar">
        <h2 className="logo">AtongAni</h2>
        <button className="nav-btn" onClick={handleProceed}>
          Login
        </button>
      </header>

      
      <section className="hero">
        <h1>Empowering Local Farmers</h1>
        <p>
          AtongAni is a digital marketplace that connects local farmers directly
          to consumers — fair prices, no middlemen.
        </p>
        <div className="hero-actions">
          <button className="primary-btn" onClick={handleProceed}>
            Get Started
          </button>
          <button className="secondary-btn" onClick={handleProceed}>
            Learn More
          </button>
        </div>
      </section>

      
      
      <section className="features">
        <div className="feature-card">
          <span className="icon">🌾</span>
          <h3>Support Farmers</h3>
          <p>Farmers earn more by selling directly to buyers.</p>
        </div>

        <div className="feature-card">
          <span className="icon">📦</span>
          <h3>Fresh Produce</h3>
          <p>Get locally sourced, fresh, and affordable goods.</p>
        </div>

        <div className="feature-card">
          <span className="icon">🤝</span>
          <h3>Fair Trade</h3>
          <p>No middlemen. Transparent and fair transactions.</p>
        </div>
      </section>

      
      <footer className="footer">
        <p>© {new Date().getFullYear()} AtongAni. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Welcome;
