from typing import Text
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), unique=True)
    user_email = Column(Text())
    user_department = Column(String(20))
    user_type = Column(String(20))
    user_password = Column(String(20))
    user_password_repeat = Column(String(20))


class Topic(Base):
    __tablename__ = "topic"

    topic_id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(Text())


class Post(Base):
    __tablename__ = "user_post"

    post_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50))
    topic_id = Column(Integer)
    post_content = Column(String(500))
    post_date = Column(String(50))


class Response(Base):
    __tablename__ = "user_response"

    response_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50))
    post_id = Column(String(50))
    response_content = Column(String(500))
    response_date = Column(String(50))

