from fastapi import FastAPI
from . routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

   
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello vamsi"}

# from .cofig import settings

# print(settings.algorithm)
# @app.get("/sqlalchemy")
# def test_posts( db : Session = Depends(get_db)):
#    posts = db.query(models.Post).all()
  
#    return {"data": posts}
   
# Dependency
#class Post(BaseModel):
    #title: str
    #content: str
    #published: bool = True
    ##rating: Optional[int] = None
# from typing import Optional,List
# from fastapi.params import Body
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from pydantic.utils import Representation
# from random import randrange
#from passlib.context import CryptContext

#pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# my_posts = [{"title":"title of post 1", "content": "content of post 1" , "id":1},{"title":"favorite food", "content": "i like pizza" , "id":2}]

# def find_post(id):
#     for p in my_posts:
#      if p['id']== id :
#       return p
# def find_index_post(id):
#    for i, p in enumerate(my_posts):
#      if p["id"]==id:
#        return i

#  #get all posts
# @app.get("/posts",response_model=list[schemas.Post])
# def get_post(db : Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     ##cursor.execute("""SELECT * FROM post""")
#     ##posts=cursor.fetchall()
#     return  posts
#     #print(posts)
#     #return {"data": my_posts}

# #create post
# @app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def create_post(post:schemas.PostCreate,db : Session = Depends(get_db)):
#     #cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
#     #new_post = cursor.fetchone()
#     #conn.commit()
#     #post_dict = post.dict()
#     #post_dict['id'] = randrange(0,10000)
#     #my_posts.append(post_dict)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# #title str, content str, category, bool published

# #get post by id
# @app.get("/posts/{id}",response_model=schemas.Post)
# def get_post(id:int,db : Session = Depends(get_db)):
#    post = db.query(models.Post).filter(models.Post.id== id).first()
#    #print(id)
#    #cursor.execute("""SELECT * FROM post WHERE id = %s""",(str(id)))
#    #post = cursor.fetchone()
#     # print(post)
#    #post = find_post(id)
#    #print(post)
#    if not post:
#     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} is not found")
#       ##respone.status_code = status.HTTP_404_NOT_FOUND
#       ##return{'Messeage': f"Post with id: {id} is not found"}
      
#    return post 


# #Delete post by id
# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int,db : Session = Depends(get_db)):
#  post = db.query(models.Post).filter(models.Post.id==id)
#     #cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""",(str(id),))
#     #deleted_post  = cursor.fetchone()
#     #conn.commit()
#   #delete post
#    # we need find the index of reqired ID in the array
#    #my_posts.pop(index)
#    #index = find_index_post(id)
  
#  if post.first() == None:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id: {id} is not found")
#    #my_posts.pop(index)
#  post.delete(synchronize_session=False)
#  db.commit()
#  return Response(status_code=status.HTTP_204_NO_CONTENT)


# #update post by id
# @app.put("/posts/{id}",response_model=schemas.Post)
# def update_post(id:int,post:schemas.PostCreate,db : Session = Depends(get_db)):
#   post_query=db.query(models.Post).filter(models.Post.id==id)
#   post_from_db= post_query.first()
#    #print(postq)
#    #cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,(str(id),)))
#    #updated_post  = cursor.fetchone()
#    #conn.commit()
#    #index = find_index_post(id)
#   if post_from_db == None:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id: {id} is not found")
#    #post_query.update({'title':'this is my updated post','content':'this is something'},synchronize_session=False)
#   post_query.update(post.dict(),synchronize_session=False)
#   db.commit()
#    #post_dict = post.dict()
#    #post_dict['id'] = id
#    #my_posts[index]= post_dict
#   return post_query.first()
   
#   #user table 


# @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_user(user : schemas.UserCreate,db:Session = Depends(get_db)):

# #hash the password - user.password
#   hashed_password  = utils.hash(user.password)
#   user.password = hashed_password

#   new_user = models.User(**user.dict())
#   db.add(new_user)
#   db.commit()
#   db.refresh(new_user)
  
#   return new_user

# @app.get('/users/{id}',response_model=schemas.UserOut)
# def get_user(id:int,db:Session = Depends(get_db)):
#  user = db.query(models.User).filter(models.User.id==id).first()
#  if not user:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id : {id} does not exist")
   
#  return user