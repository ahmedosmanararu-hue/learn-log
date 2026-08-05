// frontend/src/hooks/useFetch.jsx

import { useState, useEffect, useCallback, useMemo } from 'react';
import { useAuth } from '../context/AuthContext';

export const useFetch = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token, logout } = useAuth();

  const serializedOptions = useMemo(() => JSON.stringify(options), [options]);

  const fetchData = useCallback(async (signal) => {
    setLoading(true);
    setError(null);

    try {
      const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      };

      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }

      const response = await fetch(url, {
        signal,
        ...options,
        headers,
      });

      if (response.status === 401) {
        logout();
        throw new Error('Session expired. Please login again.');
      }

      if (!response.ok) {
        const contentType = response.headers.get('content-type') || '';
        const errorText = contentType.includes('application/json')
          ? (await response.json()).message
          : await response.text();
        throw new Error(errorText || 'Request failed');
      }

      const result = await response.json();
      setData(result);
      return result;
    } catch (err) {
      if (err.name === 'AbortError') {
        return;
      }
      setError(err.message || 'Request failed');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [url, token, logout, serializedOptions]);

  useEffect(() => {
    const controller = new AbortController();
    fetchData(controller.signal).catch(() => {});
    return () => controller.abort();
  }, [fetchData]);

  const refetch = useCallback(() => {
    const controller = new AbortController();
    fetchData(controller.signal).catch(() => {});
  }, [fetchData]);

  return { data, loading, error, refetch };
};