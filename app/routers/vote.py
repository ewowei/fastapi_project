from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from .. import schema, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote", tags=['vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db)
         , current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==
                                     vote.post_id, models.Vote.user_id == current_user.id) # type: ignore
    found_query = vote_query.first()
    if (vote.dir == 1):
        if found_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=
                                f'user {current_user.id} has already voted on post {vote.post_id}') # type: ignore
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id) # type: ignore
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_query:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        return {"message": "successfully deleted vote"}
