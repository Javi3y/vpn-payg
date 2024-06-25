import datetime
from sqlalchemy.orm import validates, relationship
from .database import Base
from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy_utils import ChoiceType, EmailType, PasswordType, URLType, UUIDType
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(EmailType, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    uuid = Column(UUIDType, server_default=text("uuid_generate_v4()"), unique=True)
    password = Column(
        PasswordType(schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]),
        nullable=False,
    )
    balance = Column(Float, nullable=False, server_default="0")
    tgid = Column(String(9), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
    is_supper_user = Column(Boolean, nullable=False, server_default="False")

    @validates("tgid")
    def validate_status(self, k, tgid):
        if not tgid.isdecimal():
            raise ValueError("OOPS,Should be in int.")
        return tgid

    def __str__(self):
        return self.username


class Inbound(Base):
    PROTOCOLS = [("vless", "vless"), ("trojan", "trojan")]

    __tablename__ = "inbounds"
    id = Column(Integer, nullable=False, primary_key=True)
    remark = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    host = Column(URLType, nullable=False)
    inbound_id = Column(Integer, nullable=False)
    session_token = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    protocol = Column(ChoiceType(PROTOCOLS))
    detail = Column(String, nullable=False, server_default=" ")
    base_link = Column(String, nullable=False)
    __table_args__ = (
        UniqueConstraint("host", "inbound_id", name="_host_inbound_id_uc"),
    )

    def __str__(self):
        return self.detail


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, nullable=False, primary_key=True)
    disabled = Column(Boolean, nullable=False, server_default="False")
    email = Column(String, nullable=False)
    uuid = Column(UUIDType, nullable=True)
    password = Column(String, nullable=True)
    usage = Column(Float, server_default="0")
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    inbound_id = Column(ForeignKey("inbounds.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (
        UniqueConstraint("user_id", "inbound_id", name="_inbound_user_uc"),
        (
            CheckConstraint(
                "(uuid IS NULL) <> (password IS NULL)", name="uuid_xor_password"
            )
        ),
    )
    user = relationship("User")
    inbound = relationship("Inbound")


class ClientUsage(Base):
    __tablename__ = "clients_usage"
    id = Column(Integer, nullable=False, primary_key=True)
    time = Column(DateTime, nullable=False)
    usage = Column(Float, nullable=False)
    last_usage = Column(Float, nullable=False)
    client_id = Column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    client = relationship("Client")
