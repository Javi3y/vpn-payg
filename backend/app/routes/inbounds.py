from typing import List
from uuid import uuid4
from fastapi import APIRouter
from sqlalchemy import select
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.xray_requests import (
    create_inbound_client,
    gb_b_converter,
    get_inbound_clients,
    get_inbound_protocol,
    get_token,
)
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
)

router = APIRouter(prefix="/inbounds", tags=["Inbounds"])


@router.post("/", response_model=schemas.InboundOut)
async def create_inbound(
    inbound: schemas.InboundIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_inbound_data = inbound.model_dump()
    if not current_user.is_supper_user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="should be supper user"
        )
    new_inbound_data["session_token"] = await get_token(
        inbound.username, inbound.host, inbound.password
    )

    if not new_inbound_data["protocol"] == "vless" or "trojan":
        new_inbound_data["protocol"] = await get_inbound_protocol(
            new_inbound_data["session_token"], inbound.host, inbound.inbound_id
        )

    new_inbound = models.Inbound(**new_inbound_data)
    db.add(new_inbound)
    await db.commit()
    await db.refresh(new_inbound)

    clients = await get_inbound_clients(
        new_inbound.session_token, new_inbound.host, new_inbound.inbound_id
    )
    for client in clients:
        tgid = client["tgId"]
        if tgid:
            user = await db.execute(select(models.User).where(models.User.tgid == str(tgid)))
            user = user.scalar()
            if user:
                if new_inbound.protocol == "vless":
                
                    new_client = models.Client(
                        uuid=client['id'], user_id=user.id, inbound_id=new_inbound.id
                    )
                elif new_inbound.protocol == "trojan":
                    new_client = models.Client(
                        password=client['password'], user_id=user.id, inbound_id=new_inbound.id
                    )
                    db.add(new_client)
                    await db.commit()

    await db.refresh(new_inbound)
    return new_inbound


@router.get("/", response_model=List[schemas.InboundOut])
async def get_inbounds(db: Session = Depends(get_db)):
    results = await db.execute(select(models.Inbound))
    return results.scalars().all()
