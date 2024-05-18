import asyncio
from httpx import AsyncClient


API_TRIES = 5
BACK_OFF = 10

async def get_token(username, host, password):
    result = ""
    tries = 0
    while not result and tries < API_TRIES:
        async with AsyncClient() as client:
            try:
                headers = {"username": username, "password": password}
                response = await client.post(host + "/login",json=headers, timeout = BACK_OFF)
                result =response.cookies.get("session")
            except Exception as e:
                print(str(e))
                tries += 1
    return result



print(asyncio.run(get_token("admin","http://127.0.0.1:2053","admin")))
