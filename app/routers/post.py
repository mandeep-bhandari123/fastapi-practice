from typing import List, Optional
from .. import models , schemas ,oauth2
from sqlalchemy import func
from sqlalchemy.orm import session 
from fastapi import  Response , status ,HTTPException , Depends ,APIRouter
from ..database import get_db 


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])

def get_all_post(db:session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int=None,skip:int=0,search:Optional[str]=""):
    
    #posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    
    
    
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createpost(post:schemas.PostCreate,db:session=Depends(get_db), curent_user:int = Depends(oauth2.get_current_user)): 
    #cursor.execute(""" INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()

    new_post=models.Post(owner_id= curent_user.id,**post.dict())
    
    
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,r:Response,db:session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id),))
    # req_post=cursor.fetchone()
    req_post=db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    if not req_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found😢")

    return req_post

@router.delete("/{id}",status_code=status.HTTP_410_GONE)
def delete_post(id:int,db:session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found😢")
    
    post_query.delete(synchronize_session=False)
    
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this task")
    
    
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found😢")

    if existing_post.owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this task")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return  post_query.first()