from .. import models,schemas, utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from .. import oauth2
from sqlalchemy import func

router = APIRouter( prefix= "/posts",tags=['Posts'])

#get all posts
# @router.get("/",response_model=List[schemas.PostOut])
@router.get("/",response_model=List[schemas.PostOut])
def get_post(db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit : int=10,skip:int=0,search:Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    ##cursor.execute("""SELECT * FROM post""")
    ##posts=cursor.fetchall()
    #print(current_user.email)
    #print(posts)
    # print(results)
    return  results
    #return {"data": my_posts}

#create post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,10000)
    #my_posts.append(post_dict)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#get post by id
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
   #post = db.query(models.Post).filter(models.Post.id== id).first()
   post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id== id).first()
   #print(id)
   #cursor.execute("""SELECT * FROM post WHERE id = %s""",(str(id)))
   #post = cursor.fetchone()
    # print(post)
   #post = find_post(id)
   #print(post)
   if not post:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} is not found")
  #  if post.owner_id != current_user.id :
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform reqested action")
      ##respone.status_code = status.HTTP_404_NOT_FOUND
      ##return{'Messeage': f"Post with id: {id} is not found"}
      
   return post 

#title str, content str, category, bool published


#Delete post by id
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
 post_query = db.query(models.Post).filter(models.Post.id==id)
    #cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""",(str(id),))
    #deleted_post  = cursor.fetchone()
    #conn.commit()
  #delete post
   # we need find the index of reqired ID in the array
   #my_posts.pop(index)
   #index = find_index_post(id)
 post = post_query.first()
 if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id: {id} is not found")
   #my_posts.pop(index)
 if post.owner_id != current_user.id :
   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform reqested action")
 post_query.delete(synchronize_session=False)
 db.commit()
 return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post by id
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
  post_query=db.query(models.Post).filter(models.Post.id==id)
  post_from_db= post_query.first()
   #print(postq)
   #cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,(str(id),)))
   #updated_post  = cursor.fetchone()
   #conn.commit()
   #index = find_index_post(id)
  
  if post_from_db == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id: {id} is not found")
  if post_from_db.owner_id != current_user.id :
   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform reqested action")
   #post_query.update({'title':'this is my updated post','content':'this is something'},synchronize_session=False)
  post_query.update(post.dict(),synchronize_session=False)
  db.commit()
   #post_dict = post.dict()
   #post_dict['id'] = id
   #my_posts[index]= post_dict
  return post_query.first()
   