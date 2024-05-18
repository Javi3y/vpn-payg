from sqlalchemy.orm import  validates
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, Integer, String
from sqlalchemy_utils import EmailType, PasswordType, URLType, UUIDType
from sqlalchemy.sql.expression import text


# class Post(Base):
#    __tablename__ = "posts"
#
#    id = Column(Integer, primary_key=True, nullable=False)
#    title = Column(String, nullable=False)
#    content = Column(String, nullable=False)
#    published = Column(Boolean, nullable=True)
#    owner_id = Column(
#        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#    )
#
#    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(EmailType, nullable=False, unique=True)
    uuid = Column(UUIDType, server_default=text("uuid_generate_v4()"), unique=True)
    password = Column(
        PasswordType(schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]),
        nullable=False,
    )
    balance = Column(Float, nullable=False, server_default="0")
    tgid = Column(String(9), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
    is_supper_user = Column(Boolean, nullable=False, server_default="False")

    @validates("tgid")
    def validate_status(self, k, tgid):
        if not tgid.isdecimal():
            raise ValueError("OOPS,Should be in int.")
        return tgid


class Inbound(Base):
    __tablename__ = "inbounds"
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    host = Column(URLType, nullable=False)
    inbound_id = Column(Integer, nullable=False)
    session_token = Column(String, nullable=False)
    price = Column(Integer, nullable=False)


# class Vote(Base):
#    __tablename__ = "votes"
#
#    user_id = Column(
#        Integer,
#        ForeignKey("users.id", ondelete="CASCADE"),
#        nullable=False,
#        primary_key=True,
#    )
#    post_id = Column(
#        Integer,
#        ForeignKey("posts.id", ondelete="CASCADE"),
#        nullable=False,
#        primary_key=True,
#    )
