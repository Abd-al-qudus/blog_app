from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    """the user class"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(300), nullable=False)
    email = Column(String(300), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    session_id = Column(String(300), nullable=False)


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    author = relationship("User", back_populates="post")
    title = Column(String(250), unique=True, nullable=False)
    subtitle = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    body = Column(Text, nullable=False)
    img_url = Column(String(250), nullable=False)
    comments = relationship('Comment', back_populates='parent_post')


class Comment(Base):
    __tablename__ = 'comments'
    id =Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    author_id =Column(Integer,ForeignKey("users.id"),nullable=False)
    comment_author = relationship("User", back_populates="comments")
    parent_post = relationship('BlogPost', back_populates='comments')
    post_id = Column(Integer, ForeignKey('blog_posts.id'))
    text = Column(Text, nullable=False)