from datetime import datetime, timedelta
from fastapi import Depends, HTTPException,status
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from . import schema,database,models
from sqlalchemy.orm import Session
from .config import settings
# We cant get the token by calling the login function in route.
# So to get the token we use a class to call the function of the route which accepts the route as arguments
oauth2_scheme= OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time

# Creating token
def create_access_token(data: dict):
    # copy the user id and user email in token into to_encode payload
    to_encode = data.copy()
    # assigning expire time to the token
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # sending the expire time to payload data 
    to_encode.update({"exp": expire})
    # creating token based on above details
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

#verifying the token by decoding and returning id 
def verify_token(token:str,credentials_exception):
    try:
        # decoding the token to get id
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])    
        id : str =payload.get("user_id")
        if id is None:
            raise credentials_exception
        # sending the id to schema
        token_data=schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

# getting the user id by calling the verify token function
def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"could not validate credentials",headers={"WWW_Authenticate":"Bearer"})
    token = verify_token(token,credentials_exception)
    # check the payload id of token who logged in with the user id in database
    user= db.query(models.User).filter(models.User.id==token.id).first()
    return user