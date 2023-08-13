#!/usr/bin/env python3
""" session_auth.py """
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """a view that handles all routes for the session authentication """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 400

    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        res = jsonify(user.to_json())
        session_name = os.getenv('SESSION_NAME')
        res.set_cookie(session_name, session_id)
        return res

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout users """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
