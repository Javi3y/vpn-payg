from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# def get_db():
#
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


# def object_as_dict(obj):
#    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
