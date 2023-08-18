#!/usr/bin/env python3
""" auth.py """
import bcrypt


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returned
    bytes which is salted hash of the input password, hashed with
    bcrypt.hashpw """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
