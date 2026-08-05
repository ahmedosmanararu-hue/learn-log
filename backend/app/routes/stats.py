# backend/app/routes/stats.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Course, Enrollment, Review

class DashboardStats(Resource):
    @jwt_required()
    def get(self):
        """Show your LEGO building progress"""
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        enrollments = Enrollment.query.filter_by(user_id=current_user_id).all()
        
        return {
            'enrollments': [e.to_dict() for e in enrollments],
            'total_courses': len(enrollments),
            'completed_courses': len([e for e in enrollments if e.status == 'completed']),
            'active_courses': len([e for e in enrollments if e.status == 'active']),
            'average_grade': sum(e.grade for e in enrollments) / len(enrollments) if enrollments else 0
        }, 200

class TopInstructors(Resource):
    def get(self):
        """Find the best LEGO teachers"""
        instructors = User.query.filter(
            User.role == 'instructor',
            User.courses_teaching.any()
        ).all()
        
        results = []
        for instructor in instructors:
            courses = instructor.courses_teaching
            if courses:
                avg_rating = sum(c.average_rating() for c in courses) / len(courses)
                results.append({
                    'instructor_id': instructor.id,
                    'email': instructor.email,
                    'course_count': len(courses),
                    'average_rating': round(avg_rating, 1)
                })
        
        results.sort(key=lambda x: x['average_rating'], reverse=True)
        
        return {'top_instructors': results[:10]}, 200