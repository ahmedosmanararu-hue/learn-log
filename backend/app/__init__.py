# backend/app/__init__.py

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.models import db, bcrypt

# Import our routes (the doorways)
from app.routes.auth import Register, Login
from app.routes.courses import CourseList, CourseDetail, CourseEnroll
from app.routes.enrollments import EnrollmentUpdate
from app.routes.reviews import ReviewList, ReviewDetail
from app.routes.stats import DashboardStats, TopInstructors

def create_app():
    # Create the Flask app - like setting up our LEGO workspace
    app = Flask(__name__)
    app.config.from_object(Config)

    #Enable CORS for cross-origin requests from Vercel frontend
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://*.vercel.app"]}})
    
    # Initialize our tools
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    
    
    # Create the API
    api = Api(app)
    
    # Add all our routes (doorways)
    # Auth routes - like the front door
    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')
    
    # Course routes - like the library
    api.add_resource(CourseList, '/courses')
    api.add_resource(CourseDetail, '/courses/<int:course_id>')
    api.add_resource(CourseEnroll, '/courses/<int:course_id>/enroll')
    
    # Enrollment routes - like the sign-up desk
    api.add_resource(EnrollmentUpdate, '/enrollments/<int:enrollment_id>')
    
    # Review routes - like the feedback box
    api.add_resource(ReviewList, '/reviews')
    api.add_resource(ReviewDetail, '/reviews/<int:review_id>')
    
    # Stats routes - like the scoreboard
    api.add_resource(DashboardStats, '/dashboard/stats')
    api.add_resource(TopInstructors, '/instructors/top')
    
    return app