
import { api } from "./client";

export const registerCustomer = (data) => api.post("/api/auth/register/customer/", data);
export const registerFarmer = (data) => api.post("/api/auth/register/farmer/", data);
export const login = (data) => api.post("/api/auth/login/", data);
export const me = () => api.get("/api/auth/me/");
