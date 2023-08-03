from fastapi import FastAPI, Response,APIRouter, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, utils

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash_function(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schema.UserOut)
def get_user(id :int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user