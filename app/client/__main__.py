import asyncio

from app.client.chat_client import ChatClient
from app.client.context import config, log

if __name__ == '__main__':
    try:
        configed_name = config['client']['name']
        name = configed_name if configed_name else input('Enter client name:')
        loop = asyncio.get_event_loop()
        client = ChatClient(name, loop)
        asyncio.ensure_future(client.chat_client())
        loop.run_forever()
    except (SystemExit, KeyboardInterrupt):
        log.debug('closing app')
        exit(0)
