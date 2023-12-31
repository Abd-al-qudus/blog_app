"""
    this module handles database operations
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import typing

from .models import Base, BlogPost, User, Comment

class DATABASE:
    """the database"""
    
    def __init__(self) -> None:
        self._engine = create_engine("sqlite:///blog.db", echo=True)
        # Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None
    
    @property
    def _session(self) -> Session:
        """create a session for the database operation"""
        if self.__session is None:
            DB_Session = sessionmaker(bind=self._engine, expire_on_commit=False)
            self.__session = DB_Session()
        return self.__session
    
    def create_user_with_email(self, email: str, password: str, full_name: str) -> User:
        """create the user with email and password and return the user"""
        new_user = User(full_name=full_name, email=email, password=password, session_id=None)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        return new_user
    
    def get_user(self, **kwargs) -> User:
        """get the user either by id, session_id or other fields"""
        if not kwargs:
            raise InvalidRequestError('arguments not specified')
        user_table_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in user_table_columns:
                raise ValueError(f"missing key {key}")
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("user not found")
        return user   
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """update the users information"""
        if not kwargs:
            raise InvalidRequestError('arguments not specified')
        user_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in user_columns:
                raise ValueError(f"missing key {key}")
        try:
            user = self.get_user(id=user_id)
            for k, v in kwargs.items():
                setattr(user, k, v)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        
    def delete_user(self, user_id: int) -> None:
        """delete the user"""
        try:
            user = self.get_user(id=user_id)
            self._session.delete(user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
