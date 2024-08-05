from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """User Model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    task = relationship("Task", back_populates="author")
    permission = relationship("Permission", back_populates="user")


class Task(Base):
    """Task Model"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    complete = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="task")
    permission = relationship("Permission", back_populates="task")


class Permission(Base):
    """Task Permission Model"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    update = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="permission")
    task = relationship("Task", back_populates="permission")
