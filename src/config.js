/**
 * Backend API URL configuration.
 *
 * In development:  VITE_API_URL=http://localhost:8000  (in .env.local)
 * In production:   VITE_API_URL=https://your-app.onrender.com  (in Vercel env vars)
 *
 * Set VITE_API_URL in Vercel project settings once your Render backend is live.
 */
export const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";
