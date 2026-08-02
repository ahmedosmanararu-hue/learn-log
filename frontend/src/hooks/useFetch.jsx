// frontend/src/hooks/useFetch.jsx

import { useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from '../context/AuthContext';

export const useFetch = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token, logout } = useAuth();
  
  // Add a ref to prevent multiple fetches
  const isMounted = useRef(true);
  const fetchCount = useRef(0);

  const fetchData = useCallback(async () => {
    // Prevent multiple simultaneous fetches
    if (fetchCount.current > 0) {
      console.log('Skipping duplicate fetch');
      return;
    }
    
    fetchCount.current += 1;
    setLoading(true);
    setError(null);

    try {
      const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      console.log('Fetching:', url);

      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (response.status === 401) {
        console.log('Token expired, logging out');
        logout();
        throw new Error('Session expired. Please login again.');
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Request failed');
      }

      const result = await response.json();
      
      if (isMounted.current) {
        setData(result);
      }
    } catch (err) {
      console.error('Fetch error:', err);
      if (isMounted.current) {
        setError(err.message);
      }
    } finally {
      if (isMounted.current) {
        setLoading(false);
      }
      fetchCount.current = 0;
    }
  }, [url, options, token, logout]);

  useEffect(() => {
    // Reset fetch count when URL changes
    fetchCount.current = 0;
    fetchData();
    
    // Cleanup function
    return () => {
      isMounted.current = false;
    };
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
};