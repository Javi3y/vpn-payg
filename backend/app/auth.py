from sqlalchemy import select
from .database import get_db
from datetime import datetime, timedelta, UTC

from fastapi.security.oauth2 import OAuth2PasswordBearer

from jose import JWTError, jwt

from .config import settings
from . import schemas

from fastapi import Depends, HTTPException, status


from . import schemas, models

from sqlalchemy.orm import Session
from .database import get_db

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


async def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


async def verity_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"www-Authenticate": "Bearer"},
    )
    user_token = await verity_access_token(token, credentials_exception)
    results = await db.execute(
        select(models.User).where(models.User.id == user_token.id)
    )
    return results.scalar()
