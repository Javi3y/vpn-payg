from enum import Enum
from typing import Optional, Union
from pydantic import (
    UUID4,
    BaseModel,
    EmailStr,
)


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


class UserUpdate(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None
    uuid: Union[UUID4, None] = None
    tgid: Union[str, None] = None
    balance: Union[float, None] = None


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


class InboundUpdate(BaseModel):
    remark: Union[str, None] = None
    price: Union[int, None] = None
    detail: Union[str, None] = None
    username: Union[str, None] = None
    password: Union[str, None] = None
    host: Union[str, None] = None
    inbound_id: Union[int, None] = None
    base_link: Union[str, None] = None


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
