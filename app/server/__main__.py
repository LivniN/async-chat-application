import asyncio

from app.server.chat_server import ChatServer
from app.server.context import config, log

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        server = ChatServer(ip=config['server']['ip'], port=int(config['server']['port']), loop=loop)
        asyncio.ensure_future(server.chat_server())
        loop.run_forever()
    except KeyboardInterrupt:
        log.debug('caught KeyboardInterrupt')
        exit(0)
