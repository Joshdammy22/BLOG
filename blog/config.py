import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Convert to int, with default value 587
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', '').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER =  os.environ.get('MAIL_DEFAULT_SENDER')
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", default="very-important")
