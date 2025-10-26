import json
from nats.aio.client import Client as NATS


class NATHandler:
    _instance = None
    _nc = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self):
        if self._nc is None or self._nc.is_closed:
            self._nc = NATS()
            await self._nc.connect("nats://localhost:4222")
            print("Connected to NATS")

    async def request(self, subject: str, payload: dict, timeout: int = 2):
        await self.connect()
        data = json.dumps(payload).encode()
        msg = await self._nc.request(subject, data, timeout=timeout)
        return json.loads(msg.data.decode())

    async def get_user_info(self, payload: dict):
        return await self.request("user.get.info", payload)

    async def close(self):
        if self._nc and not self._nc.is_closed:
            await self._nc.drain()
            await self._nc.close()


async def get_data_from_nats(payload: dict):
    nat_client = NATHandler()
    data = await nat_client.get_user_info(payload)
    return data['data'] if data['data'] else None
