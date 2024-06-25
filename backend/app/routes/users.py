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


@router.get("/profile", response_model=schemas.UserOut)
async def get_profile(current_user: int = Depends(get_current_user)):
    return current_user


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
