#!/usr/bin/python3
from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage_exception(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Handler for 404 errors.
    Returns a response indicating 'Not found'.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = '0.0.0.0' if not getenv('HBNB_API_HOST') else getenv('HBNB_API_HOST')
    port = 5000 if not getenv('HBNB_API_PORT') else int(getenv('HBNB_API_PORT'))
    app.run(host=host, port=port, threaded=True)
