import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'your-secret-key-here'  # In production, use environment variable
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memorymesh.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret-key'  # In production, use environment variable
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
