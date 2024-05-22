import sys
from app import db
from app.models import Usuarios
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

authentication = Blueprint('authentication', __name__)

@authentication.route('/register', methods=['POST'])
def register():
    username = request.json.get("username")
    passowrd = request.json.get("passowrd")

    user = Usuarios.query.filter_by(username=username).one_or_none()

    if user is not None:
        return jsonify(message='Usuário existente.')
    
    hashed_passowrd = generate_password_hash(passowrd)

    user = Usuarios(username=username, passowrd=hashed_passowrd)
    db.session.add(user)
    db.session.commit()

    return jsonify(message='Usuário criado!')

@authentication.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    passowrd = request.json.get("passowrd")
    
    user = Usuarios.query.filter_by(username=username).one_or_none()

    if user is not None and check_password_hash(user.password, passowrd):
        access_token = create_access_token(identity=username)
        response = jsonify(message='Sucesso!', access_token=access_token)
        return response, 200
    else:
        return jsonify(message='Falha no login'), 401
    
