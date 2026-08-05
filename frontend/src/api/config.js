// Default to local backend during development; override with VITE_API_URL in .env
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';
