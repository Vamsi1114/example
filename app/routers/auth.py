from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,models,schema,utils,oauth2


router=APIRouter(tags=['Authentication'])

@router.post("/login",response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # to check the user is present
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                        detail=f"user with {user_credentials.username} was not found")
    # to verify the password
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail=f"INVALID Credentials")
    # create token 
    # return token to repsonse model
    access_token = oauth2.create_access_token(data={"user_id":user.id,"user_email":user.email})
    return {"access_token":access_token,"token_type":"Bearer"}