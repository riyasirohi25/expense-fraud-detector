import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://expense_user:ro2504se@localhost/expense_fraud_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
