from enum import Enum
import inspect
from typing import Annotated, Optional, no_type_check
from pydantic import (
    UUID4,
    BaseModel,
    EmailStr,
    HttpUrl,
    PrivateAttr,
    computed_field,
    Field,
)

from app.xray_requests import b_gb_converter

# token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


# users


class User(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(User):
    password: str
    tgid: str


class UserOut(User):
    id: int
    uuid: UUID4
    balance: float
    tgid: str


class UserLogin(User):
    password: str


# inbound
class ProtocolEnum(str, Enum):
    vless = "vless"
    trojan = "trojan"


class Protocol(BaseModel):
    value: str


class Inbound(BaseModel):
    remark: str
    price: int
    detail: str

    class Config:
        from_attributes = True


class InboundIn(Inbound):
    username: str
    password: str
    host: str
    inbound_id: int
    protocol: Optional[str]
    base_link: str


class InboundOut(Inbound):
    id: int
    protocol: Protocol


# Clients


class Client(BaseModel):
    pass


class ClientIn(Client):
    inbound: int


class ClientOut(Client):
    id: int
    inbound: InboundOut
    uuid: Optional[UUID4]
    password: Optional[str]
    usage: float
