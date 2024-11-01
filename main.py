from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form, HTTPException
from typing import Annotated
from fastapi.encoders import jsonable_encoder

from model import User, Post, Topic, Response
import schema
from database import SessionLocal, engine
import model


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI()
# model.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


'''@app.get("/")
def read_root():
    return {"message": "welcome to FastAPI!"}'''


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(User).all()
    return templates.TemplateResponse("index.html", {"request": request, "data": records})


# Redirect to login page
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_database_session)):
    return templates.TemplateResponse("login.html", {"request": request})


# Redirect to register page
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request, db: Session = Depends(get_database_session)):
    return templates.TemplateResponse("register.html", {"request": request})


# Redirect to home page (useless)
@app.get("/home", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_database_session)):
    return templates.TemplateResponse("index.html", {"request": request})


# Redirect to about page (useless)
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: Session = Depends(get_database_session)):
    return templates.TemplateResponse("about.html", {"request": request})


# Redirect to posts page
@app.get("/posts/{user_id}/{topic_id}", response_class=HTMLResponse)
async def posts(request: Request, topic_id: schema.Topic.topic_id, user_id: schema.User.user_id, db: Session = Depends(get_database_session)):
    user_id = user_id
    topic_id = topic_id
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()
    user = db.query(User).filter(User.user_id == user_id).first()
    print(f"The topic id is {topic_id}")
    #user_posts = db.query(Post).filter(Post.topic_id == topic_id).all()
    user_posts = db.query(Post.post_id, Post.user_id, Post.topic_id, Post.post_content, Post.post_date, User.user_name, User.user_type, User.user_email).join(User, Post.user_id == User.user_id).filter(Post.topic_id == topic_id).all()
    print(f"User email is {user.user_email}")

    # print(f" The user id here is {user_posts.user_id}")
    #user_responses = db.query(Response).filter(Response.post_id == user_posts.post_id).all()
    #print(user_posts)
    '''for post in user_posts:
        print(f" The post id is {post.post_id}")
        user_responses = db.query(Response).filter(Response.post_id == post.post_id).all()
        return templates.TemplateResponse("posts.html", {"request": request, "user_responses": user_responses, "topic_id": topic_id, "user_id": user_id, "user_posts": user_posts})'''
    return templates.TemplateResponse("posts.html", {"request": request, "topic_id": topic_id, "user_id": user_id, "user_posts": user_posts, "topic": topic, "user": user})


# redirect to response page
@app.get("/responses/{user_id}/{topic_id}/{post_id}", response_class=HTMLResponse)
async def responses(request: Request, topic_id: schema.Topic.topic_id, user_id: schema.User.user_id, post_id: schema.Post.post_id, db: Session = Depends(get_database_session)):
    user_id = user_id
    topic_id = topic_id
    post_id = post_id
    user = db.query(User).filter(User.user_id == user_id).first()
    #user_post = db.query(Post).filter(Post.post_id == post_id).first()
    user_post = db.query(Post.post_id, Post.user_id, Post.topic_id, Post.post_content, Post.post_date, User.user_name, User.user_type, User.user_email).join(User, Post.user_id == User.user_id).filter(Post.post_id == post_id).first()
    #user_responses = db.query(Response).filter(Response.post_id == post_id).all()
    user_responses = db.query(Response.user_id, Response.post_id, Response.response_id, Response.response_content, Response.response_date, User.user_name, User.user_type).join(User, Response.user_id == User.user_id).filter(Response.post_id == post_id).all()
    print(f"User-id in response method is {user_id}, post-id id{post_id}")
    return templates.TemplateResponse("response.html", {"request": request, "topic_id": topic_id, "user": user, "user_id": user_id, "post_id": post_id, "user_post": user_post, "user_responses": user_responses})


# Redirect to login page(after registration) (useless)
@app.get("/user/{user_email}", response_class=HTMLResponse)
def read_item(request: Request, user_email: schema.User.user_email, db: Session = Depends(get_database_session)):
    item = db.query(User).filter(User.user_email == user_email).first()
    return templates.TemplateResponse("login.html", {"request": request, "user": item})


# Redirect to topic page(after login)
@app.get("/user/{user_email}/topics", response_class=HTMLResponse)
def read_item(request: Request, user_email: schema.User.user_email, db: Session = Depends(get_database_session)):
    item = db.query(User).filter(User.user_email == user_email).first()
    user_id = item.user_id
    user_name = item.user_name
    print(user_id)
    topics = db.query(Topic).all()
    # for topic in topics:
    # print (topic.topic_name)
    return templates.TemplateResponse("topic.html", {"request": request, "topics": topics, "user_id": user_id, "user_name": user_name})


# Registering a new user
@app.post("/user/")
async def create_user(db: Session = Depends(get_database_session), user_name: schema.User.user_name = Form(...), user_email: schema.User.user_email = Form(...), user_department: schema.User.user_department = Form(...), user_type: schema.User.user_type = Form(...), user_password: schema.User.user_password = Form(...), user_password_repeat: schema.User.user_password_repeat = Form(...)):
    user = User(user_name=user_name, user_email=user_email, user_department=user_department, user_type=user_type, user_password=user_password, user_password_repeat=user_password_repeat)
    db.add(user)
    db.commit()
    db.refresh(user)
    # return {"message": "Registration successful."}
    response = RedirectResponse(f'/', status_code=303)
    return response


# User Login
@app.post("/user/login")
async def login_user(db: Session = Depends(get_database_session), user_email = Form(...), user_password = Form(...)):
    # return {"message": f"Post Successful{user_email} and password {user_password} "}
    check_email = db.query(User).filter(User.user_email == user_email).first()
    check_password = db.query(User).filter(User.user_password == user_password).first()
    response = RedirectResponse(f'/user/{user_email}/topics', status_code=303)
    if check_email and check_password:
        # return {"message": f"Login Successful- {user_email} and password-  {user_password} "}
        return response
    else:
        return {"message": "E-mail or password is incorrect"}
        # raise HTTPException(status_code=404, detail="E-mail or password is incorrect")'''


# Registering a new post
@app.post("/post/")
async def create_post(db: Session = Depends(get_database_session), post_content=Form(...), topic_name=Form(...), user_id= Form(...)):
    topics = db.query(Topic).filter(Topic.topic_name == topic_name).first()
    print(f"User Id is: {user_id}")
    post = Post(post_content=post_content, user_id=user_id, topic_id=topics.topic_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    # return {"message": " Post Registration successful."}
    response = RedirectResponse(f'/posts/{user_id}/{topics.topic_id}', status_code=303)
    return response


# Register a response
@app.post("/response")
async def create_response(db: Session = Depends(get_database_session), response_content=Form(...), user_id=Form(...), topic_id=Form(...), post_id=Form(...)):
    #print (f"Post Id is {post_id}")
    post_response = Response(response_content=response_content, user_id=user_id, post_id=post_id)
    db.add(post_response)
    db.commit()
    db.refresh(post_response)
    response = RedirectResponse(f'/responses/{user_id}/{topic_id}/{post_id}', status_code=303)
    return response

















