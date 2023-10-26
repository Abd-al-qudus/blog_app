"""
    This module handles the user authentication
    """

from utils import (
    generate_id,
    generate_password_hash
)
from database import DATABASE
from models import User
from sqlalchemy.exc import NoResultFound
import bcrypt


class AUTH:
    """handles user authentication"""
    
    def __init__(self) -> None:
        self._database = DATABASE()
    
    def register(self, email: str, password: str) -> User:
        """create a new user"""
        if not isinstance(email, str) or not isinstance(password, str):
            raise ValueError("email/password must be a string")
        try:
            existing_user = self._database.get_user(email=email)
            if existing_user is not None:
                raise ValueError(f'user {email} already exist')
        except NoResultFound:
            password_hash = generate_password_hash(password)
            new_user = self._database.create_user_with_email(
                email=email,
                password=password_hash
            )
            return new_user
    
    def validate_login(self, email: str, password: str) -> bool:
        """validate the user login credentials"""
        if not isinstance(email, str) or not isinstance(password, str):
            raise ValueError("email/password must be a string")
        try:
            user = self._database.get_user(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.password
                )
        except NoResultFound:
            return False
    
    def login(self, email: str, password: str) -> None:
        """login"""
        
    def logout(self, user_id: int) -> None:
        """logout"""
