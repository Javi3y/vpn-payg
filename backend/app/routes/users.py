from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

from app.xray_requests import b_gb_converter, gb_b_converter, update_client_limit

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"user": new_user.email}


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(
    current_user: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    if not current_user.is_supper_user:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="user isn't user user"
        )
    users = await db.execute(select(models.User))
    return users.scalars().all()


@router.patch("/", response_model=schemas.UserOut)
async def update_user(
    updated_user: schemas.UserUpdate,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_dict = updated_user.model_dump(exclude_unset=True)
    print(user_dict)
    for key, value in user_dict.items():
        setattr(current_user, key, value)
    print(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/profile", response_model=schemas.UserOut)
async def get_profile(current_user: int = Depends(get_current_user)):
    return current_user


@router.get("/is_admin")
async def is_admin(current_user: int = Depends(get_current_user)):
    return current_user.is_supper_user


@router.post("/balance")
async def add_balance(
    amount: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    amount = current_user.balance + amount
    current_user.balance = amount
    await db.commit()
    await db.refresh(current_user)
    clients = await db.execute(
        select(models.Client)
        .where(models.Client.user_id == current_user.id)
        .options(selectinload(models.Client.inbound))
    )
    clients = clients.scalars()
    for client in clients:
        inbound = client.inbound
        limit = int(
            client.usage + gb_b_converter(current_user.balance / client.inbound.price)
        )
        if inbound.protocol == "vless":
            await update_client_limit(
                session=inbound.session_token,
                host=inbound.host,
                inbound_id=inbound.inbound_id,
                protocol=inbound.protocol,
                uuid=client.uuid,
                limit=limit,
            )
        elif inbound.protocol == "trojan":
            await update_client_limit(
                session=inbound.session_token,
                host=inbound.host,
                inbound_id=inbound.inbound_id,
                protocol=inbound.protocol,
                password=client.password,
                limit=limit,
            )
    return current_user.balance
