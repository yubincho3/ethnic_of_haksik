import websockets
import asyncio
import json

class WebsocketClient:
    def __init__(self, url: str):
        self.__loop = asyncio.new_event_loop()
        self.__loop.run_until_complete(self.__connect(url))

    async def __connect(self, url: str):
        self.__websock = await websockets.connect(url) # type: ignore

    async def __recv(self):
        self.__packet = await self.__websock.recv()

    async def __send(self, packet):
        await self.__websock.send(packet) # type: ignore

    def sendString(self, string):
        future = self.__send(string)
        self.__loop.run_until_complete(future)

    def getString(self) -> str:
        self.__loop.run_until_complete(self.__recv())
        return self.__packet
