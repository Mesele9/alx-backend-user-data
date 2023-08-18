#!/usr/bin/env python3
""" auth.py """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returned
    bytes which is salted hash of the input password, hashed with
    bcrypt.hashpw """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """  a method that checks and register user """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        else:
            raise ValueError(f"User {email} already exists")
