from typing import List
from uuid import uuid4
from fastapi import APIRouter, Response
from sqlalchemy import select
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.xray_requests import (
    create_inbound_client,
    delete_inbound_client,
    gb_b_converter,
    get_inbound_clients,
    get_inbound_protocol,
    get_token,
)
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
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
            user = await db.execute(
                select(models.User).where(models.User.tgid == str(tgid))
            )
            user = user.scalar()
            if user:
                if new_inbound.protocol == "vless":

                    new_client = models.Client(
                        uuid=client["id"], user_id=user.id, inbound_id=new_inbound.id
                    )
                elif new_inbound.protocol == "trojan":
                    new_client = models.Client(
                        password=client["password"],
                        user_id=user.id,
                        inbound_id=new_inbound.id,
                    )
                    db.add(new_client)
                    await db.commit()

    await db.refresh(new_inbound)
    return new_inbound


@router.get("/", response_model=List[schemas.InboundOut])
async def get_inbounds(db: Session = Depends(get_db)):
    results = await db.execute(select(models.Inbound))
    return results.scalars().all()


@router.delete("/{id}")
async def delete_inbound(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    if not current_user.is_supper_user:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="user isn't user user"
        )
    inbound = await db.execute(select(models.Inbound).where(models.Inbound.id == id))
    inbound = inbound.scalar()
    if not inbound:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="inbound does not exist")
    clients = await db.execute(select(models.Client).where(models.Client.inbound_id == id))
    clients = clients.scalars()
    for client in clients:

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
    await db.delete(inbound)
    await db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
