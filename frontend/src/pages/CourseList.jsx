// frontend/src/pages/CourseList.jsx

import React, { useState, useCallback, useMemo } from 'react';
import { useFetch } from '../hooks/useFetch';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const CourseList = () => {
  const [page, setPage] = useState(1);
  const [category, setCategory] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const { user } = useAuth();
  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';
  
  // Build URL with useMemo to prevent unnecessary updates
  const url = useMemo(() => {
    let baseUrl = `http://localhost:5000/courses?page=${page}&per_page=10`;
    if (category) baseUrl += `&category=${category}`;
    if (difficulty) baseUrl += `&difficulty=${difficulty}`;
    return baseUrl;
  }, [page, category, difficulty]);
  
  const { data, loading, error, refetch } = useFetch(url);

  // Use useCallback for filter handlers
  const handleCategoryChange = useCallback((e) => {
    setCategory(e.target.value);
    setPage(1);
  }, []);

  const handleDifficultyChange = useCallback((e) => {
    setDifficulty(e.target.value);
    setPage(1);
  }, []);

  const handleApplyFilters = useCallback(() => {
    refetch();
  }, [refetch]);

  if (loading) {
    return <div className="loading">Loading courses...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="course-list">
      <div className="course-header">
        <h1>Available Courses</h1>
        {isInstructor && (
          <Link to="/courses/create" className="create-button">
            Create New Course
          </Link>
        )}
      </div>
      
      <div className="filters">
        <select 
          value={category} 
          onChange={handleCategoryChange}
        >
          <option value="">All Categories</option>
          <option value="Programming">Programming</option>
          <option value="Web Development">Web Development</option>
          <option value="Database">Database</option>
          <option value="AI/ML">AI/ML</option>
        </select>
        
        <select 
          value={difficulty} 
          onChange={handleDifficultyChange}
        >
          <option value="">All Difficulties</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        
        <button onClick={handleApplyFilters} className="filter-button">
          Apply Filters
        </button>
      </div>

      <div className="courses-grid">
        {data?.courses?.length === 0 ? (
          <p>No courses found.</p>
        ) : (
          data?.courses?.map(course => (
            <div key={course.id} className="course-card">
              <h3>{course.title}</h3>
              <p className="course-description">{course.description}</p>
              <div className="course-meta">
                <span className={`difficulty ${course.difficulty}`}>
                  {course.difficulty}
                </span>
                <span className="rating">Rating: {course.average_rating || 'N/A'}</span>
                <span className="enrollments">Students: {course.enrollment_count || 0}</span>
              </div>
              <div className="course-actions">
                <Link to={`/courses/${course.id}`} className="view-button">
                  View Course
                </Link>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="pagination">
        <button 
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span>Page {page} of {data?.pages || 1}</span>
        <button 
          onClick={() => setPage(p => p + 1)}
          disabled={page === data?.pages}
        >
          Next
        </button>
      </div>
    </div>
  );
};