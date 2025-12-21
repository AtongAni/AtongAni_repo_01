
import axios from "axios";

// Vite env var (example: VITE_API_URL="https://example.com")
const baseURL = import.meta.env.VITE_API_URL || "/";

export const api = axios.create({
  baseURL,
  // If you're using cookies (session auth / CSRF), set true.
  // For JWT in headers only, keep false.
  withCredentials: false,
});

/**
 * Set or remove Authorization header globally.
 * Call setAuthToken(accessToken) after login
 * Call setAuthToken(null) on logout
 */
export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
}
