# backend/app/__init__.py

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate  # ADD THIS LINE
from app.config import Config
from app.models import db, bcrypt

# Import routes
from app.routes.auth import Register, Login
from app.routes.courses import CourseList, CourseDetail, CourseEnroll
from app.routes.enrollments import EnrollmentUpdate
from app.routes.reviews import ReviewList, ReviewDetail
from app.routes.stats import DashboardStats, TopInstructors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Initialize Flask-Migrate - ADD THIS LINE
    migrate = Migrate(app, db)
    
    # Create API routes
    api = Api(app)
    
    # Auth routes
    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')
    
    # Course routes
    api.add_resource(CourseList, '/courses')
    api.add_resource(CourseDetail, '/courses/<int:course_id>')
    api.add_resource(CourseEnroll, '/courses/<int:course_id>/enroll')
    
    # Enrollment routes
    api.add_resource(EnrollmentUpdate, '/enrollments/<int:enrollment_id>')
    
    # Review routes
    api.add_resource(ReviewList, '/reviews')
    api.add_resource(ReviewDetail, '/reviews/<int:review_id>')
    
    # Stats routes
    api.add_resource(DashboardStats, '/dashboard/stats')
    api.add_resource(TopInstructors, '/instructors/top')
    
    return app