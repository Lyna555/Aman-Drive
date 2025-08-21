from flask import request, jsonify
from models.police import Police
from models.user import User
from models.accident import Accident
from dbconfig import db
import re

from middlewares import token_required, role_required
from werkzeug.security import generate_password_hash

# Get a single police by ID
@token_required
@role_required('admin', 'police')
def get_police_by_id(current_user, police_id):
    police = Police.query.filter_by(id=police_id, user_id=current_user.id).first()
    if not police:
        return jsonify({'error': 'Police not found'}), 404
    
# Get all police stations
@token_required
@role_required('admin')
def get_all_police(current_user):
    police_list = Police.query.filter_by(user_id=current_user.id).all()
    return jsonify([p.serialize() for p in police_list]), 200

# Email reg expression
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Create user
@token_required
@role_required('admin')
def create_police(current_user):
    data = request.json
    role = data.get('role')

    if role != 'police':
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
    
    police_data = {
        'address_maps': data.get('address_maps'),
        'user_id': new_user.id
    }
    new_police = Police(**police_data)
    db.session.add(new_police)

    db.session.commit()
    return jsonify(new_user.serialize()), 201

# Update a police entry
@token_required
@role_required('admin', 'police')
def update_police(current_user, police_id):
    police = Police.query.filter_by(id=police_id, user_id=current_user.id).first()
    if not police:
        return jsonify({'error': 'Police not found'}), 404

    data = request.get_json()
    police.address_maps = data.get('address_maps', police.address_maps)

    db.session.commit()
    
    return jsonify(police.serialize()), 200

# Delete a police entry
@token_required
@role_required('admin', 'police')
def delete_police(current_user, police_id):
    police = Police.query.filter_by(id=police_id, user_id=current_user.id).first()
    if not police:
        return jsonify({'error': 'Police not found'}), 404

    db.session.delete(police)
    db.session.commit()
    return jsonify({'message': 'Police deleted successfully'}), 200

# Get all police accidents
@token_required
@role_required('police')
def get_all_police_accidents(current_user):
    police = Police.query.filter_by(user_id=current_user.id).first()
    
    if not police:
        return jsonify({'error': 'Police station not found'}), 404
    
    accidents = Accident.query.filter_by(police_id=police.id).all()
    
    if not accidents:
        return jsonify({'message': 'No accidents found for this police station'}), 200
    
    return jsonify([a.serialize() for a in accidents]), 200
