#!/usr/bin/python3
""" python script"""

from flask import jsonify, abort, make_response, request
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.state import State


@app_views.route("api/v1/states/<state_id>/cities", method="GET",
                    strict_slashes=False):
    def all_city(state_id):
        """Retrieves the list of all City objects of a State"""
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            citie_list = [city.to_dict() for city in state.cities]
        return jsonify(city_list)


@app_views.route("api/v1/states/cities/<city_id>", method="GET",
                    strict_slashes=False):
    def city_object(city_id):
        """Retrieves a City object."""
        city = storage.get(cities, city_id)
        if city is None:
            abort(404)
        else:
            return jsonify(city.to_dict())


@app_views.route("api/v1/states/cities/<city_id>", method="DELETE",
                    strict_slashes=False):
    def delete_city(city_id):
        """Deletes a City object"""
        city = storage.get(cities, city_id)
        if city is None:
            abort(404)
        else:
            city.delete()
            storage.save()
         return make_response({}, 200)


@app_views.route("api/v1/states/<state_id>/cities", method="POST",
                    strict_slashes=False):
    def city_post(state_id):
        """post a city"""
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        if "name" not in req:
            abort(400, "Missing name")
        if __state is None:
            abort(404)

        new_city = City(**post_req)
        setattr(new_city, 'state_id', state_id)
        storage.new(new_city)
        storage.save()
        return make_response(new_city.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update a city object with the provided city id"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a  JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    ignore_keys = ['id', 'created_id', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
