#!/usr/bin/env python3
""" auth.py """
import bcrypt
from db import DB
from user import User


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

    def register_user(self, email: str, password: str) -> User:
        """  a method that checks and register user """
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError(f"User {email} already exists")
        hashed_password = _hash_password(password)
        new_user = User(email=email, hashed_password=hashed_password)
        self._db._session.add(new_user)
        self._db._session.commit()
        return new_user
