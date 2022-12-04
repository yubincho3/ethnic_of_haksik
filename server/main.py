import asyncio

import websocketHandler
import websockets

from menuCrawler import crawlThisWeeksMenu

async def main():
    websocketHandler.restaurantList = crawlThisWeeksMenu()

    async with websockets.serve(
        websocketHandler.handler,
        host = '',
        port = 26656
    ):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
    print('server stopped.')
