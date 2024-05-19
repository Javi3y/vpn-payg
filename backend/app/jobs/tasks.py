import asyncio
from app.database import get_db
from app.models import Inbound
from app.xray_requests import get_token
def print_something():
    print("hello world")
    return "hello world"

async def update_session():
    db_generator = get_db()
    db = next(db_generator)
    for inbound in db.query(Inbound).all():
        inbound.session_token = await get_token(inbound.username, inbound.host, inbound.password)
        db.commit()




