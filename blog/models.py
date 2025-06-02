# models.py

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from .database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    category = Column(String, nullable=True)
    image_base64 = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="creator")
