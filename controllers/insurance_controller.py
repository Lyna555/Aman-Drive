from flask import request, jsonify
from models.insurance import Insurance
from dbconfig import db

from middlewares import role_required, token_required

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

# Create a new insurance
@token_required
@role_required('admin')
def create_insurance():
    data = request.json
    try:
        new_insurance = Insurance(**data)
        db.session.add(new_insurance)
        db.session.commit()
        return jsonify(new_insurance.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

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
