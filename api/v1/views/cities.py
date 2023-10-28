#!/usr/bin/python3
"""python script"""

from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def all_city(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route("/cities/<city_id>",
                 methods=["GET"], strict_slashes=False)
def city_object(city_id):
    """Retrieves a City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city.delete()
        storage.save()
    return make_response({}, 200)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def city_post(state_id):
    """Post a city"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    state = storage.get(State, state_id)

    new_city = City(**req)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(new_city.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update a city object with the provided city id"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
