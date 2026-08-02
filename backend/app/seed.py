# backend/app/seed.py

from app import create_app
from app.models import db, User, Profile, Course, Lesson, Enrollment, Review
from datetime import datetime, timedelta
import random

def seed_data():
    """Fill the LEGO box with starter pieces"""
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print(" Building LEGO world...")
        
        # 1. Create users
        users = []
        roles = ['student', 'student', 'student', 'instructor', 'instructor', 'admin']
        names = ['Alice', 'Bob', 'Charlie', 'Dr. Smith', 'Prof. Jones', 'Admin User']
        
        for i, (name, role) in enumerate(zip(names, roles)):
            user = User(
                email=f'{name.lower()}@example.com',
                role=role
            )
            user.set_password('password123')
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f" Created {len(users)} users")
        
        # 2. Create profiles
        profiles = [
            {'bio': 'I love learning about Python!', 'learning_preferences': 'video, hands-on'},
            {'bio': 'JavaScript is my favorite', 'learning_preferences': 'reading, projects'},
            {'bio': 'Learning web development', 'learning_preferences': 'interactive, pair programming'},
            {'bio': 'Teaching Python for 10 years', 'learning_preferences': 'lectures, examples'},
            {'bio': 'Web development expert', 'learning_preferences': 'workshops, demos'},
            {'bio': 'I run this place', 'learning_preferences': 'management, strategy'}
        ]
        
        for user, profile_data in zip(users, profiles):
            profile = Profile(
                user_id=user.id,
                bio=profile_data['bio'],
                avatar_url=f'https://api.dicebear.com/7.x/avatars/svg?seed={user.email}',
                learning_preferences=profile_data['learning_preferences']
            )
            db.session.add(profile)
        
        db.session.commit()
        print(" Created profiles")
        
        # 3. Create courses
        instructors = [u for u in users if u.role in ['instructor', 'admin']]
        
        course_data = [
            {
                'title': 'Python Programming 101',
                'description': 'Learn the basics of Python programming from scratch',
                'category': 'Programming',
                'difficulty': 'beginner'
            },
            {
                'title': 'Advanced Python Patterns',
                'description': 'Master advanced Python programming techniques',
                'category': 'Programming',
                'difficulty': 'advanced'
            },
            {
                'title': 'Web Development with React',
                'description': 'Build modern web applications with React',
                'category': 'Web Development',
                'difficulty': 'intermediate'
            },
            {
                'title': 'Database Design',
                'description': 'Learn how to design efficient databases',
                'category': 'Database',
                'difficulty': 'intermediate'
            },
            {
                'title': 'Introduction to AI',
                'description': 'Explore the fundamentals of artificial intelligence',
                'category': 'AI/ML',
                'difficulty': 'beginner'
            }
        ]
        
        courses = []
        for data in course_data:
            instructor = random.choice(instructors)
            course = Course(
                title=data['title'],
                description=data['description'],
                category=data['category'],
                difficulty=data['difficulty'],
                instructor_id=instructor.id
            )
            courses.append(course)
            db.session.add(course)
        
        db.session.commit()
        print(f" Created {len(courses)} courses")
        
        # 4. Create lessons
        lessons = []
        for course in courses:
            for i in range(3):
                lesson = Lesson(
                    course_id=course.id,
                    title=f'Lesson {i+1}: {course.title} Part {i+1}',
                    content=f'This is the content for lesson {i+1} of {course.title}',
                    order=i+1
                )
                lessons.append(lesson)
                db.session.add(lesson)
        
        db.session.commit()
        print(f" Created {len(lessons)} lessons")
        
        # 5. Create enrollments
        students = [u for u in users if u.role == 'student']
        
        for student in students:
            num_enrollments = random.randint(2, 3)
            selected_courses = random.sample(courses, num_enrollments)
            
            for course in selected_courses:
                enrollment = Enrollment(
                    user_id=student.id,
                    course_id=course.id,
                    grade=random.randint(60, 95),
                    status=random.choice(['active', 'completed']),
                    enrolled_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.session.add(enrollment)
        
        db.session.commit()
        print(" Created enrollments")
        
        # 6. Create reviews
        for student in students:
            num_reviews = random.randint(1, 2)
            enrollments = Enrollment.query.filter_by(user_id=student.id).all()
            
            if enrollments:
                selected_enrollments = random.sample(enrollments, min(num_reviews, len(enrollments)))
                for enrollment in selected_enrollments:
                    review = Review(
                        user_id=student.id,
                        course_id=enrollment.course_id,
                        rating=random.randint(3, 5),
                        comment=f'Great course! I learned a lot about {enrollment.course.title}'
                    )
                    db.session.add(review)
        
        db.session.commit()
        print(" Created reviews")
        
        print(" LEGO world is ready! All pieces are in place.")
        
        # Show stats
        print("\n STATS:")
        print(f"  Users: {User.query.count()}")
        print(f"  Courses: {Course.query.count()}")
        print(f"  Lessons: {Lesson.query.count()}")
        print(f"  Enrollments: {Enrollment.query.count()}")
        print(f"  Reviews: {Review.query.count()}")

if __name__ == '__main__':
    seed_data()