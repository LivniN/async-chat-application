import asyncio
import select
import sys
import termios
import time
import tty

from app.client.context import config, log


class ChatClient:
    def __init__(self, name, loop):
        self.name = name
        self.reader, self.writer = None, None
        self.loop = loop
        self.connected = False

    async def chat_client(self):
        try:
            ip = config['server']['ip']
            port = int(config['server']['port'])
            log.info(f"trying to connect to server, ip:{ip},port:{port}")
            self.reader, self.writer = await asyncio.open_connection(
                ip, port)
            self.connected = True
        except ConnectionRefusedError:
            log.error("server is not ready")
            exit(1)
        self.writer.write(f"{time.time()},{self.name}".encode())
        asyncio.ensure_future(self.get_input())
        asyncio.ensure_future(self.receive())

    async def receive(self):
        while self.connected:
            data = await self.reader.read(100)
            if not data:
                log.info(f"disconnected from server")
                self.connected = False
                break
            print(data.decode())

    @asyncio.coroutine
    def get_input(self):
        while self.connected:
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setcbreak(sys.stdin.fileno())
                buffer = ''
                while self.connected:
                    check_for_input = yield from self.loop.run_in_executor(None, self.is_data)
                    if check_for_input:
                        new = sys.stdin.read(1)
                        if new == '\x0a':
                            self.writer.write(f"{time.time()},{buffer}".encode())
                            buffer = ''
                        else:
                            buffer += new
                            print(buffer)
                break
            finally:
                try:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    raise SystemExit
                except ValueError:
                    log.warn("probably forced to shut down")

    def is_data(self):
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
