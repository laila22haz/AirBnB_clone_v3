#!/usr/bin/python3
from models.base_model import BaseModel
from models import storage
from flask import jsonify, abort
from api.v1.views import app_views
from models.state import State
from flask import request


@app_views.route('/api/v1/states', methods=['GET'])
def all_states():
    states_list = []
    states = storage.all(State).values()
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)

@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}, 200)

@app_views.route('/api/v1/states', methods=['POST'])
def create_state():
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_state = State(request_data['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict, 201)

@app_views.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' in request_data:
        state.name = request.get_json()['name']
        storage.save()
    return jsonify(state.to_dict, 200)
