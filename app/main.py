#from typing import Optional,List
from fastapi import FastAPI


#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from . import models
from .database import engine
# from sqlalchemy.orm import session
from .routers import post , user , auth


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



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():  
    return {"status": "ok"}


