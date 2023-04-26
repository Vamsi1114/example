
from fastapi import Depends, FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schema,utils
from .database import  engine,get_db
from sqlalchemy.orm import Session
from .routers import user,post,auth,vote
from fastapi.middleware.cors import CORSMiddleware
# create the table
# models.Base.metadata.create_all(bind=engine)

# create obj for FastAPI
app = FastAPI()

origins = ["https://www.google.com" ,"https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# class Post(BaseModel):
#     title:str
#     content:str
#     published: bool =True


"""
# connection to the database
try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Ganesh1608',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("DataBase connection was successful")
except Exception as error:
    print("Connecting to Database failed")
    print("Error:",error)

# To retrive data
@app.get("/")
def root():
    return {"message": "Hi Ganesh"}

@app.get("/post")
def Welcome_post():
    return {"Welcome"}

# To send data without body
@app.post("/post")
def create_post():
    return{" message:new post has been created"}
    
# To send data in body through postman and display the response

# create a post
@app.post("/post")
def create_post(payLoad: dict = Body(...)):
    # TO display data in terminal
    print(payLoad)
    #to display data in Respnse sheet
    return{"new_post": f"title: {payLoad['title']} ,content: {payLoad['content']}"}
    
#To enter data in server with a schema
@app.post("/posts")
def create_posts(post:Post):
    print(post.dict())
    return {"data": post}

# Creating app Using CRUD .This is a static memory where posts are stored

my_posts = [{"title":"title of post 1", "content": "content of post 1", "id": 1 },{"title":" title of post 2","content":"content of post 2","id": 2}]

#To get the latest post
@app.get("/posts/latest")
def get_latst_post():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
    
"""
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return {"status ": posts}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def get_post():
    return {"messaage":"Hello Ganesh"}
