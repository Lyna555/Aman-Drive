from flask import request, jsonify
from models.accident import Accident
from models.client import Client
from models.police import Police
from dbconfig import db
import requests
import re

from middlewares import role_required, token_required

from geopy.distance import geodesic

def get_lat_lng_from_gmaps(short_url):
    try:
        # Follow redirect
        response = requests.get(short_url, allow_redirects=True)
        long_url = response.url 
        
        print("Long URL:", long_url)

        # Look for @lat,lng pattern
        match = re.search(r'@([-0-9.]+),([-0-9.]+)', long_url)
        if match:
            lat, lng = match.groups()
            return (float(lat), float(lng))
        
        match = re.search(r"([-+]?\d*\.\d+),\s*([-+]?\d*\.\d+)", long_url)
        if match:
            lat = float(match.group(1))
            lng = float(match.group(2))
            return (float(lat), float(lng))

        return None
    except Exception as e:
        print("Error:", e)
        return None

def find_closest_police(accident_location):
    closest_station = None
    min_distance = float("inf")
    accident_coords = get_lat_lng_from_gmaps(accident_location)
    
    police_list = Police.query.all()
    
    print(accident_coords)

    for police in police_list:
        police_coords = get_lat_lng_from_gmaps(police.address_maps)
        distance = geodesic(accident_coords, police_coords).km
        if distance < min_distance:
            min_distance = distance
            closest_station = police

    return closest_station

# Get one accident by ID
@token_required
def get_accident(accident_id):
    accident = Accident.query.get(accident_id)
    if not accident:
        return jsonify({'error': 'Accident not found'}), 404
    
    return jsonify(accident.serialize()), 200

# Get all accidents
@token_required
@role_required('admin')
def get_all_accidents():
    accidents = Accident.query.all()
    return jsonify([a.serialize() for a in accidents]), 200

# Create a new accident
@token_required
@role_required('client')
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