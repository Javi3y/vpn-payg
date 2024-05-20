import asyncio
from httpx import AsyncClient
import json


API_TRIES = 5
BACK_OFF = 10


def gb_b_converter(gb):
    b = gb * 1073741824
    return b


async def get_token(username, host, password):
    result = ""
    tries = 0
    while not result and tries < API_TRIES:
        async with AsyncClient() as client:
            try:
                headers = {"username": username, "password": password}
                response = await client.post(
                    host + "/login", json=headers, timeout=BACK_OFF
                )
                result = response.cookies.get("session")
            except Exception as e:
                print(str(e))
                tries += 1
    return result


async def get_inbound(session, host, inbound_id):
    result = ""
    tries = 0
    url = f"{host}/panel/api/inbounds/get/{inbound_id}"
    while not result and tries < API_TRIES:
        async with AsyncClient(cookies={"session": session}) as client:
            try:
                response = await client.get(url, timeout=BACK_OFF)
                result = json.loads(response.text)
            except Exception as e:
                print(str(e))
                tries += 1
    return result


async def get_inbound_protocol(session, host, inbound_id):
    response = await get_inbound(session, host, inbound_id)
    result = response["obj"]["protocol"]
    return result


async def get_inbound_clients(session, host, inbound_id):
    response = await get_inbound(session, host, inbound_id)
    result = json.loads(response["obj"]["settings"])["clients"]
    return result


async def create_inbound_client(
    session, host, inbound_id, protocol, email, uuid, tgid, limit
):
    result = ""
    tries = 0
    while not result and tries < API_TRIES:
        async with AsyncClient(cookies={"session": session}) as client:
            try:
                if protocol == "vless":
                    clients = {
                        "clients": [
                            {"id": uuid, "email": email, "totalGB": limit, "tgId": tgid}
                        ]
                    }
                elif protocol == "trojan":
                    clients = {
                        "clients": [
                            {
                                "password": uuid,
                                "email": email,
                                "totalGB": limit,
                                "tgId": tgid,
                            }
                        ]
                    }
                clients = str(clients).replace("'", '"')
                headers = {"id": inbound_id, "settings": clients}
                response = await client.post(
                    host + "/panel/api/inbounds/addClient",
                    json=headers,
                    timeout=BACK_OFF,
                )
                print(response)
                result = response.text
            except Exception as e:
                print(str(e))
                tries += 1
    return result


# token = asyncio.run(get_token("admin", "http://127.0.0.1:2053", "admin"))
# asyncio.run(get_inbound_protocol(token, "http://127.0.0.1:2053", 1))


# print(asyncio.run(get_inbound_clients(token, "http://127.0.0.1:2053", 1)))
# print(
#    asyncio.run(
#        create_inbound_client(
#            session=token,
#            host="http://127.0.0.1:2053",
#            inbound_id=2,
#            protocol="trojan",
#            email="python-test-2",
#            uuid="dacc8086-ef7c-44fb-b363-ccaa5ca06577",
#            tgid="117728581",
#            limit=gb_b_converter(5),
#        )
#    )
# )
