import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useFetch } from '../hooks/useFetch';
import { useAuth } from '../context/AuthContext';

export const CourseDetail = () => {
  const { id } = useParams();
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const [enrolling, setEnrolling] = useState(false);
  const [enrollError, setEnrollError] = useState('');
  const [reviewData, setReviewData] = useState({ rating: 5, comment: '' });
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewError, setReviewError] = useState('');

  const { data, loading, error, refetch } = useFetch(
    `http://localhost:5000/courses/${id}`
  );

  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';
  const isOwner = data?.course?.instructor_id === user?.id;

  const handleEnroll = async () => {
    setEnrolling(true);
    setEnrollError('');
    
    try {
      const response = await fetch(`http://localhost:5000/courses/${id}/enroll`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || 'Enrollment failed');
      }

      refetch();
      alert('Successfully enrolled!');
    } catch (err) {
      setEnrollError(err.message);
    } finally {
      setEnrolling(false);
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    setSubmittingReview(true);
    setReviewError('');

    try {
      const response = await fetch('http://localhost:5000/reviews', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          course_id: parseInt(id),
          rating: reviewData.rating,
          comment: reviewData.comment
        })
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || 'Failed to submit review');
      }

      setReviewData({ rating: 5, comment: '' });
      refetch();
      alert('Review submitted successfully!');
    } catch (err) {
      setReviewError(err.message);
    } finally {
      setSubmittingReview(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this course?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/courses/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        const result = await response.json();
        throw new Error(result.message || 'Deletion failed');
      }

      navigate('/');
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  if (loading) {
    return <div className="loading">Loading course details...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (!data) {
    return <div className="error">Course not found</div>;
  }

  const course = data;

  return (
    <div className="course-detail">
      <div className="course-detail-header">
        <h1>{course.title}</h1>
        <div className="course-detail-actions">
          {isOwner && (
            <>
              <Link to={`/courses/${id}/edit`} className="edit-button">
                Edit Course
              </Link>
              <button onClick={handleDelete} className="delete-button">
                Delete Course
              </button>
            </>
          )}
        </div>
      </div>

      <div className="course-detail-content">
        <div className="course-info">
          <p className="description">{course.description}</p>
          <div className="info-grid">
            <div><strong>Category:</strong> {course.category}</div>
            <div><strong>Difficulty:</strong> {course.difficulty}</div>
            <div><strong>Instructor:</strong> {course.instructor_name || 'N/A'}</div>
            <div><strong>Average Rating:</strong> {course.average_rating || 'No ratings'}</div>
            <div><strong>Enrolled Students:</strong> {course.enrollment_count || 0}</div>
          </div>
        </div>

        <div className="lessons-section">
          <h2>Lessons</h2>
          <div className="lessons-list">
            {course.lessons?.length === 0 ? (
              <p>No lessons available.</p>
            ) : (
              course.lessons?.map(lesson => (
                <div key={lesson.id} className="lesson-item">
                  <span className="lesson-order">{lesson.order}.</span>
                  <div className="lesson-content">
                    <h4>{lesson.title}</h4>
                    <p>{lesson.content}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {user?.role === 'student' && (
          <div className="enroll-section">
            <button 
              onClick={handleEnroll} 
              disabled={enrolling}
              className="enroll-button"
            >
              {enrolling ? 'Enrolling...' : 'Enroll in this Course'}
            </button>
            {enrollError && <div className="error-message">{enrollError}</div>}
          </div>
        )}

        <div className="reviews-section">
          <h2>Reviews</h2>
          
          {user?.role === 'student' && (
            <form onSubmit={handleReviewSubmit} className="review-form">
              <h3>Write a Review</h3>
              <div className="form-group">
                <label htmlFor="rating">Rating (1-5)</label>
                <select
                  id="rating"
                  value={reviewData.rating}
                  onChange={(e) => setReviewData({ ...reviewData, rating: parseInt(e.target.value) })}
                  required
                >
                  {[1, 2, 3, 4, 5].map(r => (
                    <option key={r} value={r}>{r} stars</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="comment">Comment</label>
                <textarea
                  id="comment"
                  value={reviewData.comment}
                  onChange={(e) => setReviewData({ ...reviewData, comment: e.target.value })}
                  placeholder="Share your experience..."
                  required
                />
              </div>
              {reviewError && <div className="error-message">{reviewError}</div>}
              <button type="submit" disabled={submittingReview} className="submit-review-button">
                {submittingReview ? 'Submitting...' : 'Submit Review'}
              </button>
            </form>
          )}

          <div className="reviews-list">
            {course.reviews?.length === 0 ? (
              <p>No reviews yet. Be the first to review!</p>
            ) : (
              course.reviews?.map(review => (
                <div key={review.id} className="review-item">
                  <div className="review-header">
                    <span className="review-user">{review.user_email}</span>
                    <span className="review-rating">{'*'.repeat(review.rating)}</span>
                  </div>
                  <p className="review-comment">{review.comment}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};