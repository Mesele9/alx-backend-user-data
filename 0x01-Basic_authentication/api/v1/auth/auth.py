#!/usr/bin/env python3
""" auth.py """
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """ a class that manages the API auhtentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ a method that returns false """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if path.endswith('/') and excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
            elif path + '/' == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ a method that returns None"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ a method that returns false"""
        return None
