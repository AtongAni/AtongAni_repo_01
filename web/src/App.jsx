import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx"; // optional

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />           {/* login page */}
        <Route path="/dashboard" element={<Dashboard />} /> {/* protected page */}
      </Routes>
    </Router>
  );
}

export default App;
