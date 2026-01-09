import { api } from "./client";

// Posts endpoints
export function getPosts(params = {}) {
  return api.get("/api/posts/", { params });
}

export function createPost(data) {
  console.log("Creating post with data:", data);
  return api.post("/api/posts/", data);
}

export function updatePost(id, data) {
  return api.patch(`/api/posts/${id}/`, data);
}

export function deletePost(id) {
  return api.delete(`/api/posts/${id}/`);
}

export function getPost(id) {
  return api.get(`/api/posts/${id}/`);
}
