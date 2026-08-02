# backend/app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

# These are like our LEGO piece factories
db = SQLAlchemy()
bcrypt = Bcrypt()

# 1. USER - Like a LEGO person
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # A user has ONE profile (like each LEGO person has one hat)
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    # A user can write MANY reviews (like one person can review many LEGO sets)
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # A user can enroll in MANY courses (like one person can join many LEGO workshops)
    enrollments = db.relationship('Enrollment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # A user can teach MANY courses (if they're an instructor)
    courses_teaching = db.relationship('Course', backref='instructor', lazy=True)
    
    def set_password(self, password):
        """Hides the password so nobody can read it"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Checks if the password is correct"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Converts user to a format we can send to the frontend"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 2. PROFILE - Extra details about a person
class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bio = db.Column(db.Text, default='')
    avatar_url = db.Column(db.String(255), default='')
    learning_preferences = db.Column(db.String(255), default='')
    
    def to_dict(self):
        return {
            'id': self.id,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'learning_preferences': self.learning_preferences,
            'user_id': self.user_id
        }

# 3. COURSE - Like a LEGO instruction book
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # One course has MANY lessons
    lessons = db.relationship('Lesson', backref='course', lazy=True, cascade='all, delete-orphan')
    
    # One course has MANY reviews
    reviews = db.relationship('Review', backref='course', lazy=True, cascade='all, delete-orphan')
    
    # MANY students can be in ONE course (through enrollments)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def average_rating(self):
        """Calculates the average rating like averaging LEGO build scores"""
        if not self.reviews:
            return 0
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)
    
    def enrollment_count(self):
        """Counts how many students are in the course"""
        return len(self.enrollments)
    
    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor.email if self.instructor else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'average_rating': self.average_rating(),
            'enrollment_count': self.enrollment_count()
        }
        
        if include_details:
            data['lessons'] = [lesson.to_dict() for lesson in self.lessons]
            data['reviews'] = [review.to_dict() for review in self.reviews]
            
        return data

# 4. LESSON - Steps in the instruction book
class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'content': self.content,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 5. ENROLLMENT - Signing up for a workshop
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Makes sure a student can't enroll twice
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_enrollment'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course_title': self.course.title if self.course else None,
            'grade': self.grade,
            'status': self.status,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

# 6. REVIEW - Rating a LEGO build
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Makes sure a student can't review twice
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_review'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_email': self.user.email if self.user else None,
            'course_id': self.course_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }