import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'testsecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:t0oR!s54aP@localhost/flask_jwt'
    JWT_SECRET_KEY = 'secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False