from app.models import db, Review, Course, User  # Add User here

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Review, Course

class ReviewList(Resource):
    @jwt_required()
    def post(self):
        """Create a new review"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if course exists
        course = Course.query.get(data['course_id'])
        if not course:
            return {'message': 'Course not found'}, 404
        
        # Check if user already reviewed
        existing = Review.query.filter_by(
            user_id=current_user_id,
            course_id=data['course_id']
        ).first()
        
        if existing:
            return {'message': 'Already reviewed this course'}, 400
        
        review = Review(
            user_id=current_user_id,
            course_id=data['course_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        
        db.session.add(review)
        db.session.commit()
        
        return review.to_dict(), 201

class ReviewDetail(Resource):
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (only the author or admin)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        review = Review.query.get(review_id)
        
        if not review:
            return {'message': 'Review not found'}, 404
        
        if review.user_id != current_user_id and user.role != 'admin':
            return {'message': 'You can only delete your own reviews'}, 403
        
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted successfully'}, 200