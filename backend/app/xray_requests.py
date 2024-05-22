import asyncio
from fastapi import HTTPException
from httpx import AsyncClient
import json

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)


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
                json_response = json.loads(response.text)
                if not json_response["success"]:
                    if json_response["msg"].startswith("Invalid username"):
                        raise HTTPException(
                            status_code=HTTP_401_UNAUTHORIZED, detail=json_response
                        )
                    raise HTTPException(
                        status_code=HTTP_400_BAD_REQUEST, detail=json_response
                    )
                result = response.cookies.get("session")
            except Exception as e:
                print(str(e))
                tries += 1
                if tries >= API_TRIES:
                    raise e
    return result


async def get_inbound(session, host, inbound_id):
    result = ""
    tries = 0
    url = f"{host}/panel/api/inbounds/get/{inbound_id}"
    while not result and tries < API_TRIES:
        async with AsyncClient(cookies={"session": session}) as client:
            try:
                response = await client.get(url, timeout=BACK_OFF)
                if response.status_code in range(300, 399):
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="invalid session update session",
                    )

                json_response = json.loads(response.text)
                if not json_response["success"]:
                    if json_response["msg"].startswith("Obtain Failed"):
                        raise HTTPException(
                            status_code=HTTP_404_NOT_FOUND, detail=json_response
                        )
                    raise HTTPException(
                        status_code=HTTP_400_BAD_REQUEST, detail=json_response
                    )
                result = json_response
            except Exception as e:
                print(str(e))
                tries += 1
                if tries >= API_TRIES:
                    raise e
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
    session,
    host,
    inbound_id,
    protocol,
    email,
    tgid,
    limit,
    remark,
    uuid=None,
    password=None,
):
    result = ""
    tries = 0
    while not result and tries < API_TRIES:
        async with AsyncClient(cookies={"session": session}) as client:
            try:
                client_email = remark + ' - ' + email
                if protocol == "vless":
                    clients = {
                        "clients": [
                            {
                                "id": uuid,
                                "email": client_email,
                                "totalGB": limit,
                                "tgId": tgid,
                            }
                        ]
                    }
                elif protocol == "trojan":
                    clients = {
                        "clients": [
                            {
                                "password": password,
                                "email": client_email,
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
                if not json.loads(response.text)["success"]:
                    raise HTTPException(
                        status_code=HTTP_400_BAD_REQUEST,
                        detail=json.loads(response.text),
                    )

                result = response.text
            except Exception as e:
                print(str(e))
                tries += 1
                if tries >= API_TRIES:
                    raise e
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
