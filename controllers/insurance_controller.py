from flask import request, jsonify
from models.insurance import Insurance
from models.user import User
from dbconfig import db
import re

from middlewares import role_required, token_required
from werkzeug.security import generate_password_hash

# Get all insurances
@token_required
@role_required('admin')
def get_all_insurances():
    insurances = Insurance.query.all()
    return jsonify([i.serialize() for i in insurances]), 200

# Get one insurance by ID
@token_required
@role_required('admin')
def get_insurance(insurance_id):
    insurance = Insurance.query.get(insurance_id)
    if not insurance:
        return jsonify({'error': 'Insurance not found'}), 404
    return jsonify(insurance.serialize()), 200

# Email reg expression
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Create user
@token_required
@role_required('admin')
def create_insurance(current_user):
    data = request.json
    role = data.get('role')

    if role != 'insurance':
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

    insurance_data = {
        'address': data.get('address'),
        'user_id': new_user.id
    }
    new_insurance = Insurance(**insurance_data)
    db.session.add(new_insurance)

    db.session.commit()
    return jsonify(new_user.serialize()), 201


# Update an insurance
@token_required
@role_required('admin')
def update_insurance(insurance_id):
    insurance = Insurance.query.get(insurance_id)
    if not insurance:
        return jsonify({'error': 'Insurance not found'}), 404

    data = request.json
    for key, value in data.items():
        setattr(insurance, key, value)

    db.session.commit()
    return jsonify(insurance.serialize()), 200

# Delete an insurance
@token_required
@role_required('admin')
def delete_insurance(insurance_id):
    insurance = Insurance.query.get(insurance_id)
    if not insurance:
        return jsonify({'error': 'Insurance not found'}), 404

    db.session.delete(insurance)
    db.session.commit()
    return jsonify({'message': 'Insurance deleted'}), 200
