#!/usr/bin/env python3
""" auth.py """
from flask import request
from typing import List, TypeVar


class Auth:
    """ a class that manages the API auhtentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ a method that returns false """
        return False

    def authorization_header(self, request=None) -> str:
        """ a method that returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ a method that returns false"""
        return None
