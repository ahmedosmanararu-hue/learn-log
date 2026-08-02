import os
from datetime import timedelta

class Config:
    # Database connection - like telling our app where the LEGO storage is
    SQLALCHEMY_DATABASE_URI = 'postgresql://osman:123@localhost/learnlog_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT secret - like a special key for the LEGO castle
    JWT_SECRET_KEY = 'super-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Password hashing - keeps passwords safe
    BCRYPT_LOG_ROUNDS = 13