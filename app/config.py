import os
from dotenv import load_dotenv

# Configurações do projeto
class Config:
    load_dotenv()
    # Chave secreta
    SECRET_KEY = os.getenv('SECRET_KEY')
    # URI do Database (MySQL)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # Chave do JSON Web Token
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    # Configuração do SQL Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    # Url da API
    API_URL = os.getenv('API_URL')