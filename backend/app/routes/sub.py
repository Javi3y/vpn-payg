from uuid import UUID
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_404_NOT_FOUND,
)
from fastapi.templating import Jinja2Templates

from app.xray_requests import get_inbound_clients

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/sub", tags=["Subs"])


# @router.get("/{uuid}",response_class=HTMLResponse)
@router.get("/{uuid}")
async def get_sub(uuid: UUID, request: Request, db: Session = Depends(get_db)):
    user = await db.execute(select(models.User).where(models.User.uuid == uuid))
    user = user.scalar()
    if not user:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="user does not exist")
    clients = await db.execute(
        select(models.Client).where(models.Client.user_id == user.id)
    )
    clients = clients.scalars()
    confs = []
    for client in clients:
        inbound = await db.execute(
            select(models.Inbound).where(models.Inbound.id == client.inbound_id)
        )
        inbound = inbound.scalar()
        clients = await get_inbound_clients(
            inbound.session_token, inbound.host, inbound.inbound_id
        )
        key = "id" if inbound.protocol == "vless" else "password"
        client_key = client.uuid if inbound.protocol == "vless" else client.password
        for client_conf in clients:
            if client_conf[key] == client_key:
                conf = inbound.base_link.replace(key, client_key).replace(
                    "email", client_conf["email"]
                )
                confs.append(conf)
    balance = f"vless://@0.0.0.0:0?type=tcp&security=none#balance: {user.balance}"
    return templates.TemplateResponse(
        "sub.html", {"request": request, "balance": balance, "confs": confs}
    )
