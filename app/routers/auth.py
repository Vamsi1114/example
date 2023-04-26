from fastapi import APIRouter, Depends, status,HTTPException,Response
from sqlalchemy.orm import Session
from .. import database , schemas, models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])
#login router or path operation 
@router.post('/login',response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

#   {
#      "username": "ggaggkag" 
#      "password": "jhgfeuer"
#   }
   user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

   if not user :
        raise HTTPException(detail= 'invalid credentials',status_code=status.HTTP_403_FORBIDDEN)
 
   if not utils.verify(user_credentials.password,user.password):
       raise HTTPException(detail= 'invalid credentials',status_code=status.HTTP_403_FORBIDDEN)
   
   #we create a token 
   # return the token
   acess_token = oauth2.create_access_token(data={"user_id":user.id, "user_email": user.email})

   return {"access_token" : acess_token,"token_type": "bearer"}

