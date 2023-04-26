from fastapi import FastAPI,HTTPException,Response,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schema,database,models,oauth2


router = APIRouter(prefix="/vote",tags=['Vote'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    # check the presence of post to vote
    posts = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {vote.post_id} does not exists to vote")
    # check whether voted or not
    vote_query=db.query(models.Vote).filter(models.Vote.post_id== vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted the post {vote.post_id}")
        # if not voted the post
        new_vote= models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    # To delete the vote
    else:
    # check if already deleted or not
        # if deleted
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        # if not deleted
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"successfully deleted vote"}