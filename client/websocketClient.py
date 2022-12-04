import websockets
import asyncio

# 비동기 호출이 필요한 웹소켓 객체를 동기 호출하기 위한 클래스입니다.
class WebsocketClient:
    def __init__(self, url: str):
        self.__websock = None
        self.__loop = asyncio.new_event_loop()
        self.__loop.run_until_complete(self.__connect(url))

    # 웹소켓 연결을 종료하고 이벤트 루프를 닫습니다.
    def __del__(self):
        if self.__websock and not self.__websock.closed:
            self.__loop.run_until_complete(self.__websock.close())
        self.__loop.stop()

    # 서버와 연결합니다.
    async def __connect(self, url: str):
        self.__websock = await websockets.connect(url)

    # 데이터를 수신하여 __packet 변수에 저장합니다.
    async def __recv(self):
        self.__packet = await self.__websock.recv()

    # 데이터를 송신합니다.
    async def __send(self, packet):
        await self.__websock.send(packet)

    # 문자열을 전송합니다.
    def sendString(self, string: str):
        try:
            future = self.__send(string)
            self.__loop.run_until_complete(future)
        except:
            raise ConnectionError()

    # 수신한 문자열을 반환합니다.
    def getString(self) -> str:
        try:
            self.__loop.run_until_complete(self.__recv())
            return self.__packet
        except:
            raise ConnectionError()
