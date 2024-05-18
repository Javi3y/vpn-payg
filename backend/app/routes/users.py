from fastapi import APIRouter
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db, object_as_dict
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user": new_user.email}


#@router.get("/{id}", response_model=schemas.UserOut)
#async def get_user(
#    id: int,
#    db: Session = Depends(get_db),
#):
#    user = db.query(models.User).filter_by(id=id).first()
#    if not user:
#        raise HTTPException(
#            status_code=HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist"
#        )
#
#    user = schemas.UserOut(**object_as_dict(user))
#    return user
@router.get("/profile",response_model=schemas.UserOut)
async def get_profile(current_user: int =Depends(get_current_user)):
    return current_user
