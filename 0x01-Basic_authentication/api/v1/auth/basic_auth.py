#!/usr/bin/env python3
""" basic_auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ a method that returns thr Base64 part of theAuthorization header
        """
        if authorization_header is None or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ", 1)[1]
