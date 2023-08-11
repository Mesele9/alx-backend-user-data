#!/usr/bin/env python3
"""
app.py
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
auth_type = os.getenv("AUTH_TYPE")


if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    """ a module that checks for authenttication """
    if auth is None:
        return

    allowed_paths = [
                '/api/v1/status/',
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/'
        ]

    if auth.require_auth(request.path, allowed_paths):
        authorization_header = auth.authorization_header(request)
        if authorization_header is None:
            abort(401)

        current_user = auth.current_user(request)
        if current_user is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handeler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbidden handeler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
