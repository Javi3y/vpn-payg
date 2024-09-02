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
    b_gb_converter,
    delete_inbound_client,
    gb_b_converter,
    get_client_balance,
    get_inbound_clients,
    get_inbound_protocol,
    get_token,
    reset_usage,
    update_client_limit,
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
                        email=client["email"],
                        uuid=client["id"],
                        user_id=user.id,
                        inbound_id=new_inbound.id,
                    )
                elif new_inbound.protocol == "trojan":
                    new_client = models.Client(
                        email=client["email"],
                        password=client["password"],
                        user_id=user.id,
                        inbound_id=new_inbound.id,
                    )
                    balance = await get_client_balance(
                        new_inbound.session_token, new_inbound.host, client["email"]
                    )
                    balance = b_gb_converter(balance)
                    ubalance = balance * inbound.price
                    user.balance = user.balance + ubalance
                    print("yes")
                    await db.commit()
                    await db.refresh(user)
                    await db.refresh(new_inbound)
                    print("yes")
                    await reset_usage(
                        new_inbound.session_token,
                        new_inbound.host,
                        new_inbound.inbound_id,
                        client["email"],
                    )
                    uuid = (
                        None if (new_inbound.protocol == "trojan") else client["uuid"]
                    )
                    password = (
                        None
                        if (new_inbound.protocol == "vless")
                        else client["password"]
                    )
                    print(user.balance)
                    print(new_inbound.price)
                    print(user.balance / new_inbound.price)
                    await update_client_limit(
                        session=new_inbound.session_token,
                        host=new_inbound.host,
                        inbound_id=new_inbound.inbound_id,
                        limit=int(gb_b_converter(user.balance / new_inbound.price)),
                        protocol=new_inbound.protocol,
                        uuid=uuid,
                        password=password,
                    )

                    db.add(new_client)
                    await db.commit()

    await db.refresh(new_inbound)
    return new_inbound


@router.get("/", response_model=List[schemas.InboundOut])
async def get_inbounds(
    current_user: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    results = await db.execute(select(models.Inbound))
    return results.scalars().all()


@router.get("/{id}", response_model=schemas.InboundOut)
async def get_inbound(
    id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = await db.execute(select(models.Inbound).where(models.Inbound.id == id))
    return results.scalar()


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
    clients = await db.execute(
        select(models.Client).where(models.Client.inbound_id == id)
    )
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


@router.patch("/{id}")
async def update_inbound(
    id: int,
    updated_inbound: schemas.InboundUpdate,
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

    inbound_dict = updated_inbound.model_dump(exclude_unset=True)
    for key, value in inbound_dict.items():
        setattr(inbound, key, value)
    await db.commit()
    await db.refresh(inbound)
    session_token = await get_token(
        inbound.username, inbound.host, inbound.password
    )
    setattr(inbound, "session_token",session_token)
    await db.commit()
    await db.refresh(inbound)
    return Response(status_code=HTTP_204_NO_CONTENT)


