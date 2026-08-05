# backend/app/routes/enrollments.py

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models import db, Enrollment, User

class EnrollmentUpdate(Resource):
    @jwt_required()
    def put(self, enrollment_id):
        """Update grade or status of an enrollment"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            return {'message': 'Enrollment not found'}, 404
        
        # Check if user is instructor or admin of this course
        course = enrollment.course
        if course.instructor_id != current_user_id and user.role != 'admin':
            return {'message': 'Only instructors can update grades'}, 403
        
        data = request.get_json()
        
        if 'grade' in data:
            enrollment.grade = data['grade']
        if 'status' in data:
            enrollment.status = data['status']
            if data['status'] == 'completed':
                enrollment.completed_at = datetime.utcnow()
        
        db.session.commit()
        return enrollment.to_dict(), 200