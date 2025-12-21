
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";

// Simple protected route wrapper
function ProtectedRoute({ children }) {
  const token = localStorage.getItem("access");
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Default route goes to login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Login/Register page */}
        <Route path="/login" element={<Login />} />

        {/* Protected dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Fallback for unknown routes */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
