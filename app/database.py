from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path=r"C:\Users\nishc\project\fapi\app\.env")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("Missing DATABASE_URL in environment variables")

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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
