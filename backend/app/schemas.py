from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl


# token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


# users


class User(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(User):
    password: str
    tgid: str


class UserOut(User):
    id: int
    balance: int
    tgid: str


class UserLogin(User):
    password: str

#inbound
class ProtocolEnum(str, Enum):
    vless = 'vless'
    trojan = 'trojan'

class Protocol(BaseModel):
    value:str

class Inbound(BaseModel):
    price: int
    detail: str
    class Config:
        from_attributes = True

class InboundIn(Inbound):
    username: str
    password: str
    host: HttpUrl
    inbound_id: int
    protocol: Optional[str]

class InboundOut(Inbound):
    protocol: Protocol
