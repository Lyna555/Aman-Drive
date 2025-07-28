from flask import request, jsonify
from models.user import User
from models.client import Client
from models.insurance import Insurance
from models.police import Police
from werkzeug.security import generate_password_hash, check_password_hash
from middlewares import role_required, token_required
from dbconfig import db
from dotenv import load_dotenv
import datetime
import jwt
import re
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


# Email reg expression
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Create user
@token_required
@role_required('admin', 'insurance')
def create_user(current_user):
    data = request.json
    role = data.get('role')

    if role not in ['client', 'insurance', 'police', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400

    email = data.get('email')
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    hashed_password = generate_password_hash(data.get('password'), method='pbkdf2:sha256')

    user_data = {
        'username': data.get('username'),
        'email': email,
        'phone': data.get('phone'),
        'password': hashed_password,
        'role': role
    }

    new_user = User(**user_data)
    db.session.add(new_user)
    db.session.flush()

    if role == 'client':
        insurance = Insurance.query.filter_by(user_id=current_user.id).first()
        client_data = {
            'address': data.get('address'),
            'diseases': data.get('diseases'),
            'blood_type': data.get('blood_type'),
            'insurance_nbr': data.get('insurance_nbr'),
            'vehicle_type': data.get('vehicle_type'),
            'vehicle_brand': data.get('vehicle_brand'),
            'vehicle_year': data.get('vehicle_year'),
            'vehicle_plate': data.get('vehicle_plate'),
            'horses': data.get('horses'),
            'price': data.get('price'),
            'insurance_type': data.get('insurance_type'),
            'insurance_id': insurance.id,
            'user_id': new_user.id
        }
        new_client = Client(**client_data)
        db.session.add(new_client)

    elif role == 'insurance':
        insurance_data = {
            'address': data.get('address'),
            'user_id': new_user.id
        }
        new_insurance = Insurance(**insurance_data)
        db.session.add(new_insurance)

    elif role == 'police':
        police_data = {
            'address_maps': data.get('address_maps'),
            'user_id': new_user.id
        }
        new_police = Police(**police_data)
        db.session.add(new_police)

    db.session.commit()
    return jsonify(new_user.serialize()), 201
