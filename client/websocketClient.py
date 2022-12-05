import websockets
import asyncio

# 비동기 호출이 필요한 웹소켓 객체를 동기 호출하기 위한 클래스입니다.
class WebsocketClient:
    def __init__(self, url: str):
        self.__websock = None
        loop = asyncio.get_running_loop()
        loop.run_until_complete(self.__connect(url))

    # 서버와 연결합니다.
    async def __connect(self, url: str):
        self.__websock = await websockets.connect(url)

    # 수신한 문자열을 반환합니다.
    async def getString(self):
        try:
            return await self.__websock.recv()
        except:
            raise ConnectionError()

    # 문자열을 전송합니다.
    async def sendString(self, string: str):
        try:
            await self.__websock.send(string)
        except:
            raise ConnectionError()
