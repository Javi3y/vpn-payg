from fastapi import APIRouter
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
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
    await db.commit()
    await db.refresh(new_user)
    return {"user": new_user.email}


@router.get("/profile", response_model=schemas.UserOut)
async def get_profile(current_user: int = Depends(get_current_user)):
    return current_user


@router.post("/balance")
async def add_balance(
    amount: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.balance = current_user.balance + amount
    await db.commit()
    await db.refresh(current_user)
    return current_user.balance
