from sqlalchemy import select
from app.database import get_db
from app.models import Inbound
from app.xray_requests import get_token


def print_something():
    print("hello world")
    return "hello world"


async def update_session():
    db_generator = get_db()
    db = await anext(db_generator)
    results = await db.execute(select(Inbound))
    inbounds = results.scalars().all()
    for inbound in inbounds:
        inbound.session_token = await get_token(
            inbound.username, inbound.host, inbound.password
        )
        await db.commit()
