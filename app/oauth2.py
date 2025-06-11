from jose import JWTError , jwt
from datetime import datetime , timedelta
from .  import schemas , database ,models
from fastapi import Depends, status , HTTPException 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path=r"C:\Users\nishc\project\fapi\app\.env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 6000

def create_access_token(data:dict):
    to_encode=data.copy()
    
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt



def verify_access_token(token:str, credentials_exception):
    
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id:str=payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token:str=Depends(oauth2_scheme),db :Session =Depends(database.get_db)):
    credentials_expection= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail= f"Could not verify cardentials", headers={"ww-Authenticate":"Bearer"})
    token = verify_access_token(token , credentials_expection)
    user= db.query(models.User).filter(models.User.id == token.id).first()    
    return user