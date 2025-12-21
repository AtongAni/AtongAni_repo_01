import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, me } from "../api/auth";
import { setAuthToken } from "../api/client";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus("Logging in...");

    try {
      const res = await login({ username, password });
      const access = res.data.access;

      // store token
      localStorage.setItem("access", access);
      setAuthToken(access);

      // call /me to confirm identity
      const meRes = await me();
      setStatus(`Logged in as ${meRes.data.username} (${meRes.data.role})`);

      // redirect to dashboard
      navigate("/dashboard");
    } catch (err) {
      setStatus("Login failed. Check username/password.");
    }
  }

  return (
    <div style={{ padding: 16 }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 8, maxWidth: 320 }}>
        <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
        <button type="submit">Login</button>
      </form>
      <p>{status}</p>
    </div>
  );
}
