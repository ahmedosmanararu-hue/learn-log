# backend/app/routes/courses.py

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Course, Enrollment, User

class CourseList(Resource):
    def get(self):
        """Show all LEGO instruction books"""
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        
        query = Course.query
        
        if category:
            query = query.filter_by(category=category)
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        courses = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'courses': [course.to_dict() for course in courses.items],
            'total': courses.total,
            'page': page,
            'per_page': per_page,
            'pages': courses.pages
        }, 200
    
    @jwt_required()
    def post(self):
        """Create a new LEGO instruction book (instructors only)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.role not in ['instructor', 'admin']:
            return {'message': 'Only instructors can create courses'}, 403
        
        data = request.get_json()
        
        course = Course(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            difficulty=data['difficulty'],
            instructor_id=current_user_id
        )
        
        db.session.add(course)
        db.session.commit()
        
        return course.to_dict(), 201

class CourseDetail(Resource):
    def get(self, course_id):
        """Look at one specific LEGO instruction book"""
        course = Course.query.get(course_id)
        
        if not course:
            return {'message': 'Course not found'}, 404
            
        return course.to_dict(include_details=True), 200
    
    @jwt_required()
    def put(self, course_id):
        """Update a LEGO instruction book (instructor only)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        course = Course.query.get(course_id)
        
        if not course:
            return {'message': 'Course not found'}, 404
        
        if course.instructor_id != current_user_id and user.role != 'admin':
            return {'message': 'You can only edit your own courses'}, 403
        
        data = request.get_json()
        
        for field in ['title', 'description', 'category', 'difficulty']:
            if field in data:
                setattr(course, field, data[field])
        
        db.session.commit()
        return course.to_dict(), 200
    
    @jwt_required()
    def delete(self, course_id):
        """Delete a LEGO instruction book (instructor only)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        course = Course.query.get(course_id)
        
        if not course:
            return {'message': 'Course not found'}, 404
        
        if course.instructor_id != current_user_id and user.role != 'admin':
            return {'message': 'You can only delete your own courses'}, 403
        
        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted successfully'}, 200

class CourseEnroll(Resource):
    @jwt_required()
    def post(self, course_id):
        """Sign up for a LEGO workshop (students only)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user.role != 'student':
            return {'message': 'Only students can enroll in courses'}, 403
        
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404
        
        existing = Enrollment.query.filter_by(
            user_id=current_user_id,
            course_id=course_id
        ).first()
        
        if existing:
            return {'message': 'Already enrolled in this course'}, 400
        
        enrollment = Enrollment(
            user_id=current_user_id,
            course_id=course_id,
            status='active'
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        return {
            'message': 'Enrolled successfully',
            'enrollment': enrollment.to_dict()
        }, 201