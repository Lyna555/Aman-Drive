from flask import request, jsonify
from models.client import Client
from models.user import User
from models.insurance import Insurance
from models.accident import Accident
from dbconfig import db
import re

from middlewares import token_required, role_required
from werkzeug.security import generate_password_hash

# Email reg expression
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Get all clients
@token_required
@role_required('admin')
def get_all_clients():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients]), 200

# Get all insurance clients
@token_required
@role_required('admin', 'insurance')
def get_all_insurance_clients(current_user):
    insurance = Insurance.query.filter_by(user_id=current_user.id).first()
    if not insurance:
        return jsonify({'error': 'Insurance not found'}), 404

    clients = Client.query.filter_by(insurance_id=insurance.id).all()
    
    if not clients:
        return jsonify({'message': 'No clients found for this insurance'}), 200
    return jsonify([client.serialize() for client in clients]), 200

# Get one client by ID
@token_required
@role_required('admin', 'insurance')
def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify(client.serialize()), 200

# Get client by user ID
@token_required
@role_required('client')
def get_client_by_user(current_user):
    client = Client.query.filter_by(user_id=current_user.id).first()
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify(client.serialize()), 200

# Create a new client
@token_required
@role_required('insurance')
def create_client(current_user):
    data = request.json
    role = data.get('role')

    if role != 'client':
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
    
    insurance = Insurance.query.filter_by(user_id=current_user.id).first()
    
    if not insurance:
        return jsonify({'error': 'Insurance not found'}), 404
    
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

    db.session.commit()
    return jsonify(new_user.serialize()), 201


# Update a client
@token_required
@role_required('admin', 'insurance')
def update_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    data = request.json
    for key, value in data.items():
        setattr(client, key, value)

    db.session.commit()
    return jsonify(client.serialize()), 200

# Delete a client
@token_required
@role_required('admin', 'insurance')
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted'}), 200

# Get all client accidents
@token_required
@role_required('client')
def get_all_client_accidents(current_user):
    client = Client.query.filter_by(user_id=current_user.id).first()
    
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    accidents = Accident.query.filter_by(client_id=client.id).all()
    
    if not accidents:
        return jsonify({'message': 'No accidents found for this client'}), 200
    return jsonify([a.serialize() for a in accidents]), 200
