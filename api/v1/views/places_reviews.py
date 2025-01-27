#!/usr/bin/python3
""" place doc"""

from models.base_model import BaseModel
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all review objects of a State"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ doc delete"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """doc place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    if "text" not in req:
        abort(400, "Missing text")

    new_review = Review(**req)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return make_response(new_review.to_dict(), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """doc update"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(review.to_dict(), 200)
