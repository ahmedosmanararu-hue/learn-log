# backend/app/__init__.py

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.models import db, bcrypt, User, Profile

# Import our routes (the doorways)
from app.routes.auth import Register, Login
from app.routes.courses import CourseList, CourseDetail, CourseEnroll
from app.routes.enrollments import EnrollmentUpdate
from app.routes.reviews import ReviewList, ReviewDetail
from app.routes.stats import DashboardStats, TopInstructors

def _ensure_database_ready(app):
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            sample_users = [
                ('alice@example.com', 'student', 'I love learning about Python!', 'video, hands-on'),
                ('bob@example.com', 'student', 'JavaScript is my favorite', 'reading, projects'),
                ('charlie@example.com', 'student', 'Learning web development', 'interactive, pair programming'),
                ('dr.smith@example.com', 'instructor', 'Teaching Python for 10 years', 'lectures, examples'),
                ('prof.jones@example.com', 'instructor', 'Web development expert', 'workshops, demos'),
                ('adminuser@example.com', 'admin', 'I run this place', 'management, strategy')
            ]
            for email, role, bio, learning_preferences in sample_users:
                user = User(email=email, role=role)
                user.set_password('password123')
                profile = Profile(
                    user=user,
                    bio=bio,
                    avatar_url=f'https://api.dicebear.com/7.x/avatars/svg?seed={email}',
                    learning_preferences=learning_preferences
                )
                db.session.add(user)
                db.session.add(profile)
            db.session.commit()
            print('Created sample users for deployed login.')


def create_app():
    # Create the Flask app - like setting up our LEGO workspace
    app = Flask(__name__)
    app.config.from_object(Config)

    #Enable CORS for cross-origin requests from Vercel frontend
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Allow credentials (cookies, auth headers) to be sent]}})
    
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

    _ensure_database_ready(app)
    return app