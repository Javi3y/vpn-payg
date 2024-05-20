from sqladmin.authentication import AuthenticationBackend
from fastapi import HTTPException, Request, status
from sqlalchemy import select
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.database import get_db
from app.auth import create_access_token, verity_access_token
from app import models
from app.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        db_generator = get_db()
        db = await anext(db_generator)
        username, password = form["username"], form["password"]
        user = await db.execute(select(models.User).where(models.User.email==username))
        user = user.scalar()
        if not user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="no such user"
            )
            return False
        if not (user.is_supper_user):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="not supper user"
            )
            return False

        if not user or not password == user.password:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="invalid credentails"
            )

        # Validate username/password credentials

        # And update session
        request.session.update({"token": await create_access_token({"user_id": user.id})})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials",
            headers={"www-Authenticate": "Bearer"},
        )

        user_token = await verity_access_token(token, credentials_exception)
        db_generator = get_db()
        db = await anext(db_generator)
        user = await db.execute(select(models.User).where(models.User.id==user_token.id))
        is_supper_user = user = user.scalar().is_supper_user
        

        if user_token and is_supper_user:
            return True
        else:
            return False


authentication_backend = AdminAuth(secret_key=settings.secret_key)
