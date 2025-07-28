from flask import request, jsonify
from models.client import Client
from models.insurance import Insurance
from models.accident import Accident
from dbconfig import db

from middlewares import token_required, role_required

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

# Create a new client
@token_required
@role_required('admin', 'insurance')
def create_client():
    data = request.json
    try:
        new_client = Client(**data)
        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

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
