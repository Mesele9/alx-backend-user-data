#!/usr/bin/env python3
""" auth.py """
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """ a class that manages the API auhtentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ a method that returns false """

        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ a method that returns None"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ a method that returns false"""
        return None

    def session_cookie(self, request=None):
        """ session cookie"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
