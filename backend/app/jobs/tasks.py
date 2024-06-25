import datetime
from sqlalchemy import select
from app.database import get_db
from app import models
from app.xray_requests import (
    b_gb_converter,
    disable_client,
    get_token,
    get_client_usage,
)


async def update_session():
    db_generator = get_db()
    db = await anext(db_generator)
    results = await db.execute(select(models.Inbound))
    inbounds = results.scalars().all()
    for inbound in inbounds:
        inbound.session_token = await get_token(
            inbound.username, inbound.host, inbound.password
        )
        await db.commit()


async def update_balance():
    db_generator = get_db()
    db = await anext(db_generator)
    results = await db.execute(select(models.Inbound))
    inbounds = results.scalars().all()
    for inbound in inbounds:
        clients = await db.execute(
            select(models.Client)
            .where(models.Client.inbound_id == inbound.id)
            .where(models.Client.disabled == False)
        )
        clients = clients.scalars().all()
        for client in clients:
            user = await db.execute(
                select(models.User).where(models.User.id == client.user_id)
            )
            user = user.scalar()
            usage = await get_client_usage(
                inbound.session_token, inbound.host, client.email
            )
            print("usage before calculating: " + str(usage))

            usage = usage - client.usage

            print("usage after calculating: " + str(usage))
            print("client usage before calculating: " + str(client.usage))

            client.usage = usage + client.usage

            await db.commit()
            await db.refresh(client)
            await db.refresh(user)
            await db.refresh(inbound)
            print("client usage after calculating: " + str(client.usage))

            print("user balance before calculating: " + str(user.balance))

            await db.refresh(user)
            await db.refresh(client)
            await db.refresh(inbound)
            user.balance = user.balance - b_gb_converter(usage) * inbound.price

            await db.commit()
            await db.refresh(user)
            await db.refresh(client)
            await db.refresh(inbound)

            print("user balance after calculating: " + str(user.balance))

            if user.balance <= 5000:
                disabling_clients = await db.execute(
                    select(models.Client).where(models.Client.user_id == user.id)
                )
                for disabling_client in disabling_clients.scalars().all():
                    await disable_client(
                        inbound.session_token,
                        inbound.host,
                        inbound.inbound_id,
                        inbound.protocol,
                        password=disabling_client.password,
                    )
                    disabling_client.disabled = True
                    await db.commit()
                    await db.refresh(user)
                    await db.refresh(client)
                    await db.refresh(inbound)


async def update_usage():
    db_generator = get_db()
    db = await anext(db_generator)
    results = await db.execute(select(models.Inbound))
    inbounds = results.scalars().all()
    for inbound in inbounds:
        clients = await db.execute(
            select(models.Client).where(models.Client.inbound_id == inbound.id)
        )
        clients = clients.scalars().all()
        for client in clients:
            client_usage = await db.execute(
                select(models.ClientUsage)
                .where(models.ClientUsage.client_id == client.id)
                .order_by(models.ClientUsage.time.desc())
            )
            client_usage = client_usage.scalars().first()
            last_usage = client.usage
            if client_usage:
                usage = last_usage - client_usage.last_usage
                new_usage = models.ClientUsage(
                    time=datetime.datetime.now(),
                    usage=usage,
                    last_usage=last_usage,
                    client_id=client.id,
                )
            else:
                new_usage = models.ClientUsage(
                    time=datetime.datetime.now(),
                    usage=last_usage,
                    last_usage=0,
                    client_id=client.id,
                )
            db.add(new_usage)

            await db.commit()
            await db.refresh(client)
            await db.refresh(new_usage)
