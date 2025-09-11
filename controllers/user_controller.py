from flask import request, jsonify
from models.user import User
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from middlewares import token_required
from dotenv import load_dotenv
from dbconfig import db
import datetime
import jwt
import os

load_dotenv()

secret = os.getenv('SECRET_KEY')

# Login
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = jwt.encode(
        {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        secret,
        algorithm="HS256"
    )   

    return jsonify({
        'access_token': access_token,
        'user': user.serialize()
    }), 200
    

# Get a specific user
@token_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.serialize())

# Change password
@token_required
def change_password(user_id, current_password, new_password):
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"
    
    if not check_password_hash(user.password, current_password):
        return False, "Current password is incorrect"
    
    user.password = generate_password_hash(new_password)

    db.session.commit()

    return True, "Password updated successfully"
