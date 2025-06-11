from .. import models , schemas ,utils
from sqlalchemy.orm import session
from fastapi import FastAPI , Response , status ,HTTPException , Depends ,APIRouter
from ..database import get_db
from typing import List
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate ,db:session=Depends(get_db)):
    
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int, db:session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id{id} not found")
    return user
    

@router.get("/",response_model=List[schemas.UserOut])
def get_all_user(db:session=Depends(get_db)):
    users = db.query(models.User).all()
    return users