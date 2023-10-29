#!/usr/bin/python3
"""app file"""
from flask import app, Flask, make_response, jsonify, abort, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """handles teardown appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', "0.0.0.0")
    port = int(getenv('HBNB_API_PORT', "0.0.0.0"))
    app.run(host=host, port=port, threaded=True)
