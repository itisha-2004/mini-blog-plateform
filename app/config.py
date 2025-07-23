import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/blog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
