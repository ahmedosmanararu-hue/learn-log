# backend/app/routes/auth.py

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models import db, User, Profile

class Register(Resource):
    def post(self):
        """Like signing up for a LEGO club membership"""
        data = request.get_json()
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400
        
        # Create new user
        user = User(
            email=data['email'].strip().lower(),
            role=data.get('role', 'student')
        )
        user.set_password(data['password'])
        
        # Create profile for user
        profile = Profile(
            bio=data.get('bio', ''),
            avatar_url=data.get('avatar_url', ''),
            learning_preferences=data.get('learning_preferences', '')
        )
        
        user.profile = profile
        db.session.add(user)
        db.session.commit()
        
        return {
            'message': 'User created successfully',
            'user': user.to_dict()
        }, 201

class Login(Resource):
    def post(self):
        """Like showing your LEGO club membership card"""
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(data['password']):
            return {'message': 'Invalid email or password'}, 401
        
        # Create JWT tokens - use string identities so JWT subject claims are valid
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200