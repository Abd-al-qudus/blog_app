"""
    This module handles the user authentication
    """

from api.utils import (
    generate_id,
    generate_password_hash
)
from .database import DATABASE
from .models import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
import bcrypt


class AUTH:
    """handles user authentication"""
    
    def __init__(self) -> None:
        self._database = DATABASE()
    
    def register(self, email: str, password: str, full_name: str) -> User:
        """create a new user"""
        if not all(isinstance(value, str) for value in (email, password, full_name)):
            raise ValueError("email/password/full name must be a string")
        try:
            existing_user = self._database.get_user(email=email)
            if existing_user is not None:
                raise ValueError(f'user {email} already exist')
        except NoResultFound:
            password_hash = generate_password_hash(password)
            new_user = self._database.create_user_with_email(
                email=email,
                password=password_hash,
                full_name=full_name
            )
            return new_user
    
    def validate_login(self, email: str, password: str) -> bool:
        """Validate the user login credentials"""
        if not all(isinstance(value, str) for value in (email, password)):
            raise ValueError("email/password must be a string")
        try:
            user = self._database.get_user(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.password)
        except NoResultFound:
            return False
    
    def login(self, email: str, password: str) -> str:
        """log the user in and create session token"""
        if self.validate_login(email, password):
            session_id = generate_id()
            user = self._database.get_user(email=email)
            self._database.update_user(user.id, session_id=session_id)
            return session_id  
        else:
            raise ValueError("Invalid login credentials")        

    def logout(self, user_id: int) -> None:
        """log out and delete the session"""
        if not isinstance(user_id, int):
            raise ValueError('user id must be integer')
        self._database.update_user(user_id, session_id=None)
        
    def session_manager(self) -> Session:
        """manage the auth session"""
        return self._database._session

    def get_auth_session_user(self, **kwargs) -> User:
        """get the user using auth sessions"""
        if not kwargs:
            raise ValueError('Search keywords must not be empty')
        return self._database.get_user(**kwargs)
