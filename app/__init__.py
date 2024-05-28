from flask import Flask
from .config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)



SWAGGER_URL = '/api/docs'  
API_URL = "/static/openapi.json" 

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={  
        'app_name': "Embrapa Vitibrasil API"
    },

)


from app import models
from app.routes import routes
from app.auth import auth

app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(routes, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
