import asyncio
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.jobs.tasks import update_session
from .auth import create_access_token, get_current_user

from . import models, schemas
from .routes import users, inbounds, clients, sub


from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
)
from sqladmin import Admin
from .admin.views import ClientAdmin, UserAdmin, InboundAdmin

from .database import get_db, engine
from .admin.admin import authentication_backend

from .jobs.my_jobs import scheduler


app = FastAPI()

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(InboundAdmin)
admin.add_view(ClientAdmin)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(inbounds.router)
app.include_router(clients.router)
app.include_router(sub.router)

scheduler.start()


@app.post("/login")
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    results = await db.execute(
        select(models.User).where(models.User.email == user_credentials.username)
    )
    user = results.scalar()
    if not user or not user_credentials.password == user.password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="invalid credentails"
        )
    access_token = await create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

