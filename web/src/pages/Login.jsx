
import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login, me, registerCustomer, registerFarmer } from "../api/auth";
import { setAuthToken } from "../api/client";

export default function Login() {
  const navigate = useNavigate();

  const [mode, setMode] = useState("login"); // "login" | "register"

  // shared fields
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // register-only fields
  const [email, setEmail] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("customer"); // "customer" | "farmer"

  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  // Optional: if already logged in, go straight to dashboard
  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      setAuthToken(token);
      navigate("/dashboard");
    }
  }, [navigate]);

  function resetMessages() {
    setStatus("");
    setError("");
  }

  function switchMode(nextMode) {
    resetMessages();
    setMode(nextMode);

    // optional: clear passwords when switching modes
    setPassword("");
    setConfirmPassword("");
  }

  function extractError(err, fallback) {
    // Try common DRF error shapes
    const data = err?.response?.data;
    if (!data) return fallback;

    if (typeof data === "string") return data;
    if (data.detail) return data.detail;

    // Field errors: { email: ["..."], username: ["..."] }
    const firstKey = Object.keys(data)[0];
    if (firstKey && Array.isArray(data[firstKey])) return data[firstKey][0];

    return fallback;
  }

  async function handleLoginSubmit(e) {
    e.preventDefault();
    resetMessages();
    setStatus("Logging in...");

    try {
      const res = await login({ username, password });
      const access = res.data.access;

      localStorage.setItem("access", access);
      setAuthToken(access);

      // confirm identity / load role for display
      const meRes = await me();
      setStatus(`Logged in as ${meRes.data.username} (${meRes.data.role})`);

      navigate("/dashboard");
    } catch (err) {
      setStatus("");
      setError(extractError(err, "Login failed. Check username/password."));
    }
  }

  async function handleRegisterSubmit(e) {
    e.preventDefault();
    resetMessages();

    if (!email.trim()) {
      setError("Email is required.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setStatus("Creating account...");

    try {
      const payload = { username, email, password };

      // ✅ Match your backend endpoints:
      // /api/auth/register/customer/ OR /api/auth/register/farmer/
      if (role === "farmer") {
        await registerFarmer(payload);
      } else {
        await registerCustomer(payload);
      }

      setStatus("Account created! Logging you in...");

      // Auto-login after register
      const res = await login({ username, password });
      const access = res.data.access;

      localStorage.setItem("access", access);
      setAuthToken(access);

      await me(); // verifies token + loads user
      navigate("/dashboard");
    } catch (err) {
      setStatus("");
      setError(extractError(err, "Registration failed. Try a different username/email."));
    }
  }

  return (
    <div style={{ maxWidth: 420, margin: "40px auto", padding: 16 }}>
      <h2 style={{ marginBottom: 12 }}>
        {mode === "login" ? "Login" : "Create Account"}
      </h2>

      {mode === "login" ? (
        <form onSubmit={handleLoginSubmit}>
          <div style={{ marginBottom: 10 }}>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
              autoComplete="username"
              style={{ width: "100%", padding: 10 }}
              required
            />
          </div>

          <div style={{ marginBottom: 10 }}>
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="password"
              type="password"
              autoComplete="current-password"
              style={{ width: "100%", padding: 10 }}
              required
            />
          </div>

          <button type="submit" style={{ width: "100%", padding: 10 }}>
            Login
          </button>

          <div style={{ marginTop: 12 }}>
            <small>
              No account?{" "}
              <button
                type="button"
                onClick={() => switchMode("register")}
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#2563eb",
                  cursor: "pointer",
                  padding: 0,
                }}
              >
                Create one
              </button>
            </small>
          </div>
        </form>
      ) : (
        <form onSubmit={handleRegisterSubmit}>
          <div style={{ marginBottom: 10 }}>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
              autoComplete="username"
              style={{ width: "100%", padding: 10 }}
              required
            />
          </div>

          <div style={{ marginBottom: 10 }}>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="email"
              type="email"
              autoComplete="email"
              style={{ width: "100%", padding: 10 }}
              required
            />
          </div>

          {/* ✅ Role selector to match customer/farmer endpoints */}
          <div style={{ marginBottom: 10 }}>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              style={{ width: "100%", padding: 10 }}
            >
              <option value="customer">Customer</option>
              <option value="farmer">Farmer</option>
            </select>
          </div>

          <div style={{ marginBottom: 10 }}>
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="password"
              type="password"
              autoComplete="new-password"
              style={{ width: "100%", padding: 10 }}
              required
            />
          </div>

          <div style={{ marginBottom: 10 }}>
            <input
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="confirm password"
              type="password"
              autoComplete="new-password"
              style={{ width: "100%", padding: 10 }}
              required
            />
          </div>

          <button type="submit" style={{ width: "100%", padding: 10 }}>
            Register
          </button>

          <div style={{ marginTop: 12 }}>
            <small>
              Already have an account?{" "}
              <button
                type="button"
                onClick={() => switchMode("login")}
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#2563eb",
                  cursor: "pointer",
                  padding: 0,
                }}
              >
                Login
              </button>
            </small>
          </div>
        </form>
      )}

      {status ? (
        <p style={{ marginTop: 14, color: "#0f766e" }}>{status}</p>
      ) : null}
      {error ? (
        <p style={{ marginTop: 14, color: "#b91c1c" }}>{error}</p>
      ) : null}

      <div style={{ marginTop: 16 }}>
        <small>
          <Link to="/login" style={{ color: "#64748b" }}>
            Back
          </Link>
        </small>
      </div>
    </div>
  );
}
