#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    count_object = {}
    count_object['amenities'] = storage.count(Amenity)
    count_object['cities'] = storage.count(City)
    count_object['places'] = storage.count(Place)
    count_object['reviews'] = storage.count(Review)
    count_object['states'] = storage.count(State)
    count_object['users'] = storage.count(User)
    return jsonify(count_object)
