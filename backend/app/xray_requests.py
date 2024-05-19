import asyncio
from httpx import AsyncClient
import json


API_TRIES = 5
BACK_OFF = 10


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


async def get_inbound_protocol(session, host, inbound_id):
    result = ""
    tries = 0
    url = f"{host}/panel/api/inbounds/get/{inbound_id}"
    print(url)
    while not result and tries < API_TRIES:
        async with AsyncClient(cookies={"session": session}) as client:
            try:
                response = await client.get(url, timeout=BACK_OFF)
                result = response
                result = (json.loads(result.text)['obj']['protocol'])
            except Exception as e:
                print(str(e))
                tries += 1
    return result


#token = asyncio.run(get_token("admin", "http://127.0.0.1:2053", "admin"))
#asyncio.run(get_inbound_protocol(token, "http://127.0.0.1:2053", 1))
