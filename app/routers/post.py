from .. import models,schema,oauth2
from fastapi import Depends, FastAPI, Response,status,HTTPException,APIRouter
from ..database import  engine,get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router =APIRouter(prefix="/posts",tags=['Posts'])

# Getting all posts
#@router.get("/",response_model=List[schema.Post_response])
@router.get("/",response_model=List[schema.PostOut])
def get_All_post(db:Session =Depends(get_db),current_user=Depends(oauth2.get_current_user),
                 limit:int=10,skip:int=0,search:str=""):
   # cursor.execute("""SELECT * FROM posts""")
   # posts =cursor.fetchall()
   # return {"data":posts}
    print(current_user.id)
#retreving data from database by sqlalchemy orm   
    # posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    # if not posts:
    #     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
    #                         detail="There are no posts to display")
    # return posts
# retreving data along with number of votes
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(
        models.Post.id).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    
    print(results)
    return results


 # calling a particular post through id
#@router.get("/{id}",response_model=schema.Post_response)
@router.get("/{id}",response_model=schema.PostOut)
def get_post_BY_ID(id : int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id=%s""",(str(id)))
    # post=cursor.fetchone()
    # return{"post_details": post}
    print(current_user.email)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)      # prints the object
    # #If the id not present the status should show 404 not found
    # if not post:
    #     raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id:{id} was not found")
    # return post
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(results)
    return results


# creating post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post_response)
def create_post(post: schema.Post_create, db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
   # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)RETURNING * """,
   #               (post.title,post.content,post.published))
   # new_post =cursor.fetchone()
   # conn.commit()
   # return {"data": new_post}

#sending data to database by sqlalchemy orm
    print(current_user.email)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# deleting a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    deleted_post= post_query.first()
    
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exists")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updating post
@router.put("/{id}",response_model=schema.Post_response)
def update_post(id: int,post:schema.Post_create,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published =%s WHERE id=%s RETURNING *""", 
    #                (post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    # return {"data":updated_post.first()}
    print(current_user.email)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    
    if updated_post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post