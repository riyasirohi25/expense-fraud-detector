import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///expenses.db')  # Temporary SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
