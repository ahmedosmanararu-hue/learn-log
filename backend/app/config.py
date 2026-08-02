import os
from datetime import timedelta


class Config:
    """Application configuration.

    Uses `DATABASE_URL` environment variable when available (production),
    otherwise falls back to a local SQLite database for easy local development
    and tests.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///learnlog_dev.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT secret - replace in production via env var
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Password hashing rounds; reduce in dev for speed, increase in production
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', '12'))