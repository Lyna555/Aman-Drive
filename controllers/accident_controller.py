from flask import request, jsonify
from models.accident import Accident
from models.client import Client
from models.police import Police
from dbconfig import db

from middlewares import role_required, token_required

# Get all accidents
@token_required
@role_required('admin')
def get_all_accidents():
    accidents = Accident.query.all()
    return jsonify([a.serialize() for a in accidents]), 200

# Get one accident by ID
@token_required
def get_accident(accident_id):
    accident = Accident.query.get(accident_id)
    if not accident:
        return jsonify({'error': 'Accident not found'}), 404
    return jsonify(accident.serialize()), 200

# Create a new accident
@token_required
def create_accident():
    data = request.json
    try:
        new_accident = Accident(**data)
        db.session.add(new_accident)
        db.session.commit()
        return jsonify(new_accident.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Update an accident
@token_required
def update_accident(accident_id):
    accident = Accident.query.get(accident_id)
    if not accident:
        return jsonify({'error': 'Accident not found'}), 404

    data = request.json
    for key, value in data.items():
        setattr(accident, key, value)

    db.session.commit()
    return jsonify(accident.serialize()), 200

# Delete an accident
@token_required
def delete_accident(accident_id):
    accident = Accident.query.get(accident_id)
    if not accident:
        return jsonify({'error': 'Accident not found'}), 404

    db.session.delete(accident)
    db.session.commit()
    return jsonify({'message': 'Accident deleted'}), 200