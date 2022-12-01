import websockets
import asyncio

class WebsocketClient:
    def __init__(self, url: str):
        self.__loop = asyncio.new_event_loop()
        self.__loop.run_until_complete(self.__connect(url))

    def __del__(self):
        self.__loop.run_until_complete(self.__websock.close())
        self.__loop.stop()

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
