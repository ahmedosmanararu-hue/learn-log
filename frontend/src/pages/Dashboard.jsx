import React from 'react';
import { Link } from 'react-router-dom';
import { useFetch } from '../hooks/useFetch';
import { useAuth } from '../context/AuthContext';
import { API_BASE_URL } from '../api/config';

export const Dashboard = () => {
  const { user } = useAuth();
  const { data, loading, error } = useFetch(`${API_BASE_URL}/dashboard/stats`);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="dashboard">
      <h1>My Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Courses</h3>
          <p className="stat-number">{data?.total_courses || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Completed</h3>
          <p className="stat-number">{data?.completed_courses || 0}</p>
        </div>
        <div className="stat-card">
          <h3>In Progress</h3>
          <p className="stat-number">{data?.active_courses || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Average Grade</h3>
          <p className="stat-number">{data?.average_grade?.toFixed(1) || 'N/A'}</p>
        </div>
      </div>

      {['instructor', 'admin'].includes(user?.role) && (
        <div className="dashboard-actions">
          <Link to="/courses/create" className="create-button">
            Add New Course
          </Link>
        </div>
      )}

      <div className="enrollments-section">
        <h2>My Enrollments</h2>
        {data?.enrollments?.length === 0 ? (
          <p>You are not enrolled in any courses yet.</p>
        ) : (
          <div className="enrollments-list">
            {data?.enrollments?.map(enrollment => (
              <div key={enrollment.id} className="enrollment-item">
                <div className="enrollment-info">
                  <h4>{enrollment.course_title}</h4>
                  <div className="enrollment-details">
                    <span className={`status ${enrollment.status}`}>
                      {enrollment.status}
                    </span>
                    <span className="grade">Grade: {enrollment.grade || 'N/A'}</span>
                    <span className="date">Enrolled: {new Date(enrollment.enrolled_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};