from typing import List
from fastapi import APIRouter, Response
from sqlalchemy import select
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from uuid import uuid4
import string
import random

from app.xray_requests import (
    create_inbound_client,
    delete_inbound_client,
    gb_b_converter,
)

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/")
async def create_client(
    client: schemas.ClientIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    inbound = await db.execute(
        select(models.Inbound).where(models.Inbound.id == client.inbound)
    )
    inbound = inbound.scalar()
    if not inbound:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="inbound does not exist")
    check_client = await db.execute(
        select(models.Client)
        .where(models.Client.user_id == current_user.id)
        .where(models.Client.inbound_id == client.inbound)
    )
    check_client = check_client.scalar()
    if check_client:
        raise HTTPException(HTTP_409_CONFLICT, detail="client already exist")
    if inbound.protocol == "vless":
        uuid = str(uuid4())
        created_client = await create_inbound_client(
            session=inbound.session_token,
            host=inbound.host,
            inbound_id=inbound.inbound_id,
            protocol=inbound.protocol,
            email=current_user.username,
            uuid=uuid,
            remark=inbound.remark,
            tgid=current_user.tgid,
            limit=gb_b_converter(
                (current_user.balance / inbound.price)
                if current_user.balance > 0
                else 0.001
            ),
        )

        new_client = models.Client(
            uuid=uuid, user_id=current_user.id, inbound_id=inbound.id
        )
    elif inbound.protocol == "trojan":
        password = "".join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase)
            for _ in range(10)
        )
        created_client = await create_inbound_client(
            session=inbound.session_token,
            host=inbound.host,
            inbound_id=inbound.inbound_id,
            protocol=inbound.protocol,
            email=current_user.username,
            password=password,
            remark=inbound.remark,
            tgid=current_user.tgid,
            limit=gb_b_converter(
                (current_user.balance / inbound.price)
                if current_user.balance > 0
                else 0.001
            ),
        )
        new_client = models.Client(
            password=password, user_id=current_user.id, inbound_id=inbound.id
        )

    print(created_client)
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client


@router.delete("/{id}")
async def delete_client(
    id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    client = await db.execute(select(models.Client).where(models.Client.id == id))
    client = client.scalar()
    if not client:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="client does not exist")
    if not client.user_id == current_user.id:
        raise HTTPException(HTTP_403_FORBIDDEN, detail="user does not own client")
    inbound = await db.execute(
        select(models.Inbound).where(models.Inbound.id == client.inbound_id)
    )
    inbound = inbound.scalar()
    if inbound.protocol == "vless":
        response = await delete_inbound_client(
            session=inbound.session_token,
            host=inbound.host,
            inbound_id=inbound.inbound_id,
            protocol=inbound.protocol,
            uuid=client.uuid,
        )
    if inbound.protocol == "trojan":
        response = await delete_inbound_client(
            session=inbound.session_token,
            host=inbound.host,
            inbound_id=inbound.inbound_id,
            protocol=inbound.protocol,
            password=client.password,
        )
    await db.delete(client)
    await db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[schemas.ClientOut])
async def get_clients(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_client = await db.execute(
        select(models.Client)
        .where(models.Client.user_id == current_user.id)
        .options(selectinload(models.Client.inbound))
    )
    check_client = check_client.scalars().all()
    return check_client
