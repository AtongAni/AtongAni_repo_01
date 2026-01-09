
import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { me } from "../api/auth";
import { setAuthToken } from "../api/client";

export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/login");
      return;
    }

    setAuthToken(token);

    me()
      .then((res) => {
        setUser(res.data);
        setStatus("");
      })
      .catch((err) => {
        console.log(err);
        // token invalid/expired -> logout + go login
        localStorage.removeItem("access");
        setAuthToken(null);
        navigate("/login");
      });
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("access");
    setAuthToken(null);
    navigate("/login");
  }

  if (!user) return <div style={{ padding: 16 }}>{status}</div>;

  return (
    <div className="dashboard-container" style={{ maxWidth: 640, margin: "40px auto", padding: 16 }}>
      <h2>Welcome, {user.username}</h2>

      <div style={{ marginTop: 12, lineHeight: 1.8 }}>
        <div><b>Email:</b> {user.email}</div>
        <div><b>Role:</b> {user.role}</div>
      </div>

      <div style={{ marginTop: 18, display: "flex", gap: 12 }}>
        <button onClick={handleLogout} style={{ padding: "10px 14px" }}>
          Logout
        </button>
      </div>
    </div>
  );
}
