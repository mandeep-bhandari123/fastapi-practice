from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from .. import schemas ,database , models , oauth2
router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    vote_query=db.query(models.Votes).filter(models.Votes.post_id == vote.post_id , models.Votes.user_id == current_user.id)
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted in this post")
        new_vote = models.Votes(post_id= vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"Message":"Successfully added Vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return{"message":"Sucessfully Deleted Vote"}
        