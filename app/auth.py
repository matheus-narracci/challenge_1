from app import app, db, jwt
from app.models import Usuarios
from flask import jsonify, Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not username or not email or not password:
        return jsonify({"msg": "E-mail, usuário ou senha não existe."}), 400

    if Usuarios.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = Usuarios(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": f"Usuário {username} criado com sucesso!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"msg": "E-mail, usuário ou senha não existe."}), 400

    user = Usuarios.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return jsonify({"msg": "Usuário ou senha incorretos."}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)