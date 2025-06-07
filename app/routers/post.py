from .. import models , schemas ,oauth2
from sqlalchemy.orm import session
from fastapi import FastAPI , Response , status ,HTTPException , Depends ,APIRouter
from ..database import get_db 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createpost(post:schemas.PostCreate,db:session=Depends(get_db), get_current_user:int = Depends(oauth2.get_current_user)): 
    #cursor.execute(""" INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,r:Response,db:session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id),))
    # req_post=cursor.fetchone()
    req_post=db.query(models.Post).filter(models.Post.id==id).first()
    if not req_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found😢")
    return req_post

@router.delete("/{id}",status_code=status.HTTP_410_GONE)
def delete_post(id:int,db:session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found😢")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found😢")

    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return  post_query.first()