from typing import List
from fastapi import Depends, FastAPI, Response,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from .. import models,schema,utils,oauth2
from ..database import  engine,get_db

router =APIRouter(prefix="/users",tags=['Users'])

# creating user in User table
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
#Getting user by id
@router.get("/{id}",response_model=schema.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} was not found")
    return user

# deleting user
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.id)
    # To select the query
    user=db.query(models.User).filter(models.User.id== id)
    # To select the row
    u=user.first()
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} was not found")
    if u.id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="It is not possible not delete other user")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Getting all users
@router.get("/",response_model=List[schema.UserOut])
def get_All_users(db:Session =Depends(get_db)):
  
#retreving data from database by sqlalchemy orm   
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="There are no users to display")
    return users