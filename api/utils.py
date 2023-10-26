"""
    This module contains the helper functions needed in the authentication file
    """

import bcrypt
import uuid


def generate_password_hash(self, password: str) -> bytes:
    """generate the password has using bcrypt and """
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hash

def generate_id() -> str:
    """generate random ids"""
    return str(uuid.uuid4())
