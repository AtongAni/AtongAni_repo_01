import { useEffect, useState } from "react";
import { me } from "../api/auth";
import { setAuthToken } from "../api/client";

export default function Dashboard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) return;
    setAuthToken(token);

    me().then(res => setUser(res.data)).catch(err => console.log(err));
  }, []);

  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h1>Welcome, {user.username}</h1>
      <p>Email: {user.email}</p>
      <p>Role: {user.role}</p>
    </div>
  );
}
