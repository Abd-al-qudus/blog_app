from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    Integer
)

Base = declarative_base()

class User(Base):
    """the user class"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(300), nullable=False)
    email = Column(String(300), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    session_id = Column(String(300), nullable=False)
