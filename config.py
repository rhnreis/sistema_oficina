import os

# Configuração do banco de dados SQLite para desenvolvimento
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lantercar-secret-key-2024'
    
    # Database Configuration - SQLite para desenvolvimento
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'lantercar.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login
    LOGIN_VIEW = 'auth.login'
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

