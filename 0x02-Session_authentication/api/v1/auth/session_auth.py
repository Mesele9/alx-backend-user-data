#!/usr/bin/env python3
""" session_auth """
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ a class that inherits from Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ a method that creates a session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ an instance method that returns a User ID based on a Session Id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ an instance method that returns a User instance based on a
        cookie value """
        if request is None:
            return None

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
