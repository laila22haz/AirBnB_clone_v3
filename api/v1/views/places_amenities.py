#!/usr/bin/python3
""" place doc"""

from models.base_model import BaseModel
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"], strict_slashes=False)
def all_amenities(place_id):
    """Retrieves the list of all review objects of a State"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(place_id, amenity_id):
    """ doc delete"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    storage.delete(place)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_post(place_id, amenity_id):
    """doc place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)

    new_review = Review(**req)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return make_response(new_review.to_dict(), 201)

