import asyncio
import signal
import os

import websocketHandler
import websockets

from menuCrawler import crawlThisWeeksMenu

async def main():
    websocketHandler.restaurantList = crawlThisWeeksMenu()

    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    async with websockets.serve(
        websocketHandler.handler,
        host = '',
        port = 26656
    ):
        await stop

if __name__ == '__main__':
    asyncio.run(main())
