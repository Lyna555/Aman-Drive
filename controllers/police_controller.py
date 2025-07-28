from flask import request, jsonify
from models.police import Police
from models.accident import Accident
from dbconfig import db

from middlewares import token_required, role_required

# Create a new police record
@token_required
@role_required('admin')
def create_police(current_user):
    data = request.get_json()
    address_maps = data.get('address_maps')

    if not address_maps:
        return jsonify({'error': 'Address is required'}), 400

    police = Police(address_maps=address_maps, user_id=current_user.id)
    db.session.add(police)
    db.session.commit()

    return jsonify(police.serialize()), 201

# Get all police records (optional filtering by user)
@token_required
@role_required('admin')
def get_all_police(current_user):
    police_list = Police.query.filter_by(user_id=current_user.id).all()
    return jsonify([p.serialize() for p in police_list]), 200

# Get a single police by ID
@token_required
@role_required('admin', 'police')
def get_police_by_id(current_user, police_id):
    police = Police.query.filter_by(id=police_id, user_id=current_user.id).first()
    if not police:
        return jsonify({'error': 'Police not found'}), 404
    return jsonify(police.serialize()), 200

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
