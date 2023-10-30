#!/usr/bin/python3
""" place doc"""

from models.base_model import BaseModel
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models.place import Place
from models.user import User
from models.city import City


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all City objects of a State"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ doc delete"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """doc place"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user_id = req['user_id']

    __user = storage.get(User, user_id)
    __city = storage.get(City, city_id)
    if not __user or not __city:
        abort(404)
    if "name" not in req:
        abort(400, "Missing name")

    new_place = Place(**req)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return make_response(new_place.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """doc update"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(place.to_dict(), 200)
