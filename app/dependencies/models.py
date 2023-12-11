from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True, index=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    posts = relationship('Blog', back_populates='owner')
    
class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String, unique=True, index=True)
    content = Column(String, unique=True, index=True)
    date_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    owner = relationship('User', back_populates='posts')
    # vote = relationship('Vote', back_populates='blog')
    
class Vote(Base):
    __tablename__ = 'vote'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    blog_id = Column(Integer, ForeignKey('blog.id', ondelete='CASCADE'), primary_key=True)
    # blog = relationship('Blog', back_populates='vote')

    