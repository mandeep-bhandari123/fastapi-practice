from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends

from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas,utils
from .database import engine, get_db
from sqlalchemy.orm import session



app = FastAPI()


models.Base.metadata.create_all(bind=engine)



# while True:  
#     try:
#         conn=psycopg2.connect(host='name',database='name',user='name',password='your_passwoed',cursor_factory=RealDictCursor)
#         cursor= conn.cursor()
#         print("Sucess")
#         break
#     except Exception as err:
#         print("failed")   
#         print(err) 
#         time.sleep(2)

my_posts =[{"title":"title of post 1", "content":"content of post 1", "id":1},{"title":"title of post 2","content":"Content of post 2","id":2}
        ]

@app.get("/")
def root():  
    return {"status": "ok"}



@app.get("/posts", response_model= list[schemas.Post])
def send_post(db:session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""" )
    #posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createpost(post:schemas.PostCreate,db:session=Depends(get_db)): 
    #cursor.execute(""" INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,r:Response,db:session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id),))
    # req_post=cursor.fetchone()
    req_post=db.query(models.Post).filter(models.Post.id==id).first()
    if not req_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found😢")
    return req_post

@app.delete("/posts/{id}",status_code=status.HTTP_410_GONE)
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

@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
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



@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate ,db:session=Depends(get_db)):
    
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    return new_user

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)

def create_user(user:schemas.UserCreate ,db:session=Depends(get_db)):
    
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}',response_model=schemas.UserOut)
def get_user(id:int, db:session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id{id} not found")
    return user
    