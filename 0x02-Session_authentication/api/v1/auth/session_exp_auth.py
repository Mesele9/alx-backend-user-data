#!/usr/bin/env python3
""" session_exp_auth.py """
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta

class SessionExpAuth(SessionAuth):
    """ a class that imherits from SessionAuth """

    def __init__(self):
        """ constructor """
        session_duration = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create session id with expiration """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ return a user id based on session id with expiration """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id, None)
        if not session_dict:
            return None

        user_id = session_dict.get('user_id', None)
        created_at = session_dict.get('created_at', None)

        if self.session_duration <= 0 or not created_at:
            return user_id

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
