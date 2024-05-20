from fastapi import APIRouter
from sqlalchemy import select
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_404_NOT_FOUND,
)
from uuid import uuid4

from app.xray_requests import create_inbound_client, gb_b_converter

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
    uuid = str(uuid4())
    inbound = inbound.scalar()
    created_client = await create_inbound_client(
        session=inbound.session_token,
        host=inbound.host,
        inbound_id=inbound.inbound_id,
        protocol=inbound.protocol,
        email=current_user.username,
        uuid=uuid,
        tgid=current_user.tgid,
        limit=gb_b_converter(
            (current_user.balance / inbound.price) if current_user.balance > 0 else 0.001
        ),
    )
    print(created_client)
    new_client = models.Client(
        uuid=uuid, user_id=current_user.id, inbound_id=inbound.id
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client
