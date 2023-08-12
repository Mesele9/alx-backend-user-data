#!/usr/bin/env python3
""" basic_auth
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ a method that returns thr Base64 part of the Authorization header
        """
        if authorization_header is None or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ a method that return the decoded value of Base64 string """
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception:
            return None

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ a method that returns the user email and password from
        Base64 decoded value """
        if decoded_base64_authorization_header is None or \
           not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
                                     self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """ a method that returns the User instance based on his email
        and password """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None
