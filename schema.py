from datetime import date
from pydantic import BaseModel


class User(BaseModel):
    user_id = int
    user_name = str
    user_email = str
    user_department = str
    user_type = str
    user_password = str
    user_password_repeat = str
    # data = date
    
    class Config:
        orm_mode = True


class Topic(BaseModel):
    topic_id = int
    topic_name = str

    # data = date

    class Config:
        orm_mode = True


class Post(BaseModel):
    post_id = int
    user_id = int
    topic_id = str
    post_content = str

    # data = date

    class Config:
        orm_mode = True


class Response(BaseModel):
    response_id = int
    user_id = int
    post_id = int
    response_content = str

    # data = date

    class Config:
        orm_mode = True