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
    
    def create_user_with_email(self, email: str, password: str) -> User:
        """create the user with email and password and return the user"""
        new_user = User(email=email, password=password)
        self._session.add(new_user)
        self._session.commit()
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
        user = self.get_user(id=user_id)
        for k, v in kwargs.items():
            setattr(user, k, v)
        self._session.commit()
        
    def delete_user(self, user_id: int) -> None:
        """delete the user"""
        user = self.get_user(id=user_id)
        self._session.delete(user)
        self._session.commit()

    def get_all_posts(self) -> BlogPost:
        posts = self._session.query(BlogPost).all()
        return posts
    
    def get_posts_by_id(self, id: int) -> BlogPost:
        try:
            post = self._session.query(BlogPost).filter_by(id=id).first()
            return post
        except Exception as e:
            print(f"Error in get_posts_by_id: {str(e)}")
            return None
    
    def delete_postById(self, id: int)-> bool:
        post_to_delete = self.__session.query(BlogPost).get(id)
        try:
            self.__session.delete(post_to_delete)
            self.__session.commit()
            return True
        except:
            return False
        
    def get_all_comments(self, post_id: int) -> Comment:
        return self._session.query(Comment).filter_by(post_id=post_id).all()
    
    def add_newComments(self, text:str, comment_author:str, parent_post: int ) -> Comment:
        new_comment = Comment()
        self._session.add(new_comment)
        self._session.commit()
        return new_comment
      
