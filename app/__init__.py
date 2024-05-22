from flask import Flask
from .config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
# app.register_blueprint(api, url_prefix='/api')


from app import models
from app.routes import routes
from app.auth import auth

app.register_blueprint(routes, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/auth')
